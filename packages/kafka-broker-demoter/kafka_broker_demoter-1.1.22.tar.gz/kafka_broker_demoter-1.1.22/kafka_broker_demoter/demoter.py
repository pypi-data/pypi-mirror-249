import copy
import json
import logging
import os
import random
import string
import subprocess
import tempfile

from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer
from kafka.admin import NewTopic
from tenacity import retry, retry_if_exception_type, stop_after_delay, wait_fixed

from kafka_broker_demoter.exceptions import (
    BrokerStatusError,
    ChangeReplicaAssignmentError,
    ProduceRecordError,
    RecordNotFoundError,
    TriggerLeaderElectionError,
)

logger = logging.getLogger(__name__)


class Demoter(object):
    TOPIC_TRACKER = "__demote_tracker"

    def __init__(
        self,
        bootstrap_servers="localhost:9092",
        kafka_path="/opt/kafka",
        kafka_heap_opts="-Xmx512M",
        topic_tracker=TOPIC_TRACKER,
    ):
        self.bootstrap_servers = bootstrap_servers
        self.kafka_path = kafka_path
        self.kafka_heap_opts = kafka_heap_opts
        self.topic_tracker = topic_tracker

        self.admin_client = None
        self.partitions_temp_filepath = None
        self.admin_config_tmp_file = None
        self.admin_config_content = (
            "default.api.timeout.ms=240000\nrequest.timeout.ms=120000"
        )

    @property
    def _get_admin_client(self):
        if self.admin_client is None:
            self.admin_client = KafkaAdminClient(
                bootstrap_servers=self.bootstrap_servers
            )
        return self.admin_client

    def _get_topics_metadata(self):
        topic_metadata = self._get_admin_client.describe_topics()
        return topic_metadata

    def _get_producer(self):
        return KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            compression_type="lz4",
            retries=3,
        )

    @retry(
        stop=stop_after_delay(6),
        wait=wait_fixed(1),
        reraise=True,
        retry=retry_if_exception_type((RecordNotFoundError, ProduceRecordError)),
    )
    def _produce_record(self, key, value):
        """
        Retry producing a record with given key and value to a topic.

        Args:
            key: The key of the record.
            value: The value of the record.

        Raises:
            ProduceRecordError: If the record fails to be produced after retries.
        """
        serialized_key = str(key).encode("utf-8")
        serialized_value = json.dumps(value).encode("utf-8")
        try:
            producer = self._get_producer()
            future = producer.send(
                self.topic_tracker, key=serialized_key, value=serialized_value
            )
            future.get(timeout=10)
        except Exception as e:
            logger.warning("Failed to produce message: {}, trying again...".format(e))
            raise ProduceRecordError

        # Make sure record was saved
        self._consume_latest_record_per_key(key)

        logger.info(
            "Successful produced record with key {} and value {}".format(key, value)
        )

    def _remove_non_existent_topics(self, broker_id):
        """
        Removes non-existent topics from the list of partitions.

        Args:
            broker_id: The ID of the broker.

        Returns:
            A list of partitions that correspond to existing topics.

        Raises:
            None.

        Note:
            This method first retrieves the latest record of partition information for the given broker_id using the
            `_consume_latest_record_per_key` method. Then, it checks if any partitions are found. If not, it returns None.
            Otherwise, it retrieves the list of existing topics using the `_get_topics_metadata` method. Finally, it
            extracts the partitions that correspond to existing topics and returns them as a new list.

        """
        partitions = self._consume_latest_record_per_key(broker_id)
        if partitions is None:
            logger.debug("No partitions found for broker {}".format(broker_id))
            return None

        existing_topics = [topic["topic"] for topic in self._get_topics_metadata()]
        new_partitions = []

        for partition in partitions["partitions"]:
            topic = partition.get("topic", "")
            if topic in existing_topics:
                new_partitions.append(partition)
        return {"partitions": new_partitions}

    def _get_consumer(self):
        consumer = KafkaConsumer(
            self.topic_tracker,
            group_id=self.topic_tracker,
            enable_auto_commit=False,
            auto_offset_reset="earliest",
            bootstrap_servers=self.bootstrap_servers,
        )
        return consumer

    def _consume_latest_record_per_key(self, key):
        """
        Consume and retrieve the latest record for a given key.

        Args:
            key: The key used to filter the records.

        Returns:
            dict: The latest record payload for the given key.

        Raises:
            RecordNotFoundError: If no record is found for the given key.
        """
        consumer = self._get_consumer()
        records = consumer.poll(timeout_ms=20000)
        latest_record_payload = {}

        for topic_partition, record_list in records.items():
            for record in record_list:
                if int(record.key.decode("utf-8")) == key:
                    latest_record_payload[key] = json.loads(
                        record.value.decode("utf-8")
                    )
        consumer.close()

        if len(latest_record_payload) == 0:
            logger.warning("Latest record not found for key {}".format(key))
            raise RecordNotFoundError
        logger.debug(
            "Latest record found for key {}: {}".format(key, latest_record_payload[key])
        )
        return latest_record_payload[key]

    def _get_partition_leaders_by_broker_id(self, broker_id):
        """
        Retrieves partition leader information for a specified broker ID.

        Args:
            broker_id (int): The ID of the broker to fetch partition leaders.

        Returns:
            dict: A dictionary with partition information for the specified broker as leader.

        This method retrieves partition leader information for a specific broker in a Kafka cluster.
        It filters the topics and partitions in the cluster, storing relevant information (topic name, partition ID, and replica IDs)
        only for partitions where the specified broker is the leader.

        Note: This method relies on other helper methods, such as `_get_topics_metadata()`, to fetch the necessary metadata.

        """
        partitions = {"partitions": []}
        for topic in self._get_topics_metadata():
            topic_name = topic["topic"]
            for partition in topic["partitions"]:
                partition_id = partition["partition"]
                leader = partition["leader"]
                replicas = partition["replicas"]
                if broker_id == leader and len(replicas) > 1:
                    partitions["partitions"].append(
                        {
                            "topic": topic_name,
                            "partition": int(partition_id),
                            "replicas": [int(replica) for replica in replicas],
                        }
                    )
        return partitions

    def _get_demoting_proposal(self, broker_id, current_partitions_state):
        """
        Get a demoting proposal for the specified broker by reassigning replicas.

        Args:
            broker_id: The ID of the broker to generate the demoting proposal for.
            current_partitions_state: The current state of the partitions.

        Returns:
            dict: A demoting proposal with reassigned replicas.

        """
        demoting_plan = copy.deepcopy(current_partitions_state)
        for counter, partition in enumerate(demoting_plan["partitions"]):
            replicas = partition["replicas"]
            reassigned_replicas = [replicas[-1]] + replicas[:-1]
            demoting_plan["partitions"][counter]["replicas"] = reassigned_replicas
        return demoting_plan

    def _create_topic(self):
        """
        Create a new topic for tracking broker demotion rollback, if it doesn't already exist.

        Returns:
            None

        """
        topics = self._get_admin_client.list_topics()
        if self.topic_tracker not in topics:
            logger.info(
                "Creating a new topic called {} for tracking broker demotion rollback".format(
                    self.topic_tracker
                )
            )
            topic = NewTopic(
                name=self.topic_tracker,
                num_partitions=1,
                replication_factor=3,
                topic_configs={"cleanup.policy": "compact"},
            )
            self._get_admin_client.create_topics(
                new_topics=[topic], validate_only=False
            )

    def demote(self, broker_id):
        """
        Demotes a broker by reassigning the partition leaders from the specified broker to other brokers.
        If an ongoing or unfinished demote operation is found for the broker, a BrokerStatusError is raised.
        If a RecordNotFoundError occurs while checking for ongoing demote operations, the broker is considered ready for demotion.

        Args:
            broker_id (int): The ID of the broker to be demoted.

        Returns:
            None: If the broker is already demoted and no partition leaders are found.
        """
        self._create_topic()
        try:
            if self._consume_latest_record_per_key(broker_id) is not None:
                raise BrokerStatusError(
                    "Ongoing or unfinished demote operation was found for broker {}".format(
                        broker_id
                    )
                )
        except RecordNotFoundError:
            logger.debug(
                "Ongoing or unfinished demote operation was not found for broker {}, proceeding to demote the broker".format(
                    broker_id
                )
            )

        current_partitions_state = self._get_partition_leaders_by_broker_id(broker_id)
        if not current_partitions_state["partitions"]:
            logger.info(
                "Broker {} already demoted, no partition leaders found".format(
                    broker_id
                )
            )
            return None
        else:
            demoted_partitions_state = self._get_demoting_proposal(
                broker_id, current_partitions_state
            )
            self._change_replica_assignment(demoted_partitions_state)
            self._trigger_leader_election(demoted_partitions_state)
            self._save_rollback_plan(broker_id, current_partitions_state)

    def demote_rollback(self, broker_id):
        """
        Perform a rollback for the previous demote operation on a specific broker.

        Args:
            broker_id: The ID of the broker to rollback the demotion for.

        Raises:
            BrokerStatusError: If the previous demote operation on the broker was not found.

        Returns:
            None
        """
        previous_partitions_state = self._remove_non_existent_topics(broker_id)
        if previous_partitions_state is None:
            raise BrokerStatusError(
                "Previous demote operation on broker {} was not found, there is nothing to rollback".format(
                    broker_id
                )
            )
        self._change_replica_assignment(previous_partitions_state)
        self._trigger_leader_election(previous_partitions_state)
        self._produce_record(broker_id, None)
        logger.info(
            "Rollback plan for broker {} was successfully executed".format(broker_id)
        )

    def _generate_tempfile_with_json_content(self, data):
        """
        Generates a temporary file with the specified JSON content.

        Args:
            data (dict): A dictionary representing the JSON content.

        Returns:
            str: The filepath of the generated temporary file.

        Raises:
            None.

        Notes:
            - If `self.partitions_temp_filepath` is already set, a new temporary file will not be generated.
            - The generated filepath will have a random filename consisting of lowercase letters and digits.
            - The generated filepath will have the '.json' extension.

        """
        if self.partitions_temp_filepath is None:
            filename = "".join(
                random.choices(string.ascii_lowercase + string.digits, k=10)
            )
            self.partitions_temp_filepath = tempfile.mktemp(
                suffix=".json", prefix=filename
            )

        with open(self.partitions_temp_filepath, "w") as temp_file:
            json.dump(data, temp_file)
            return self.partitions_temp_filepath

    def _change_replica_assignment(self, demoting_plan):
        """
        Change the replica assignment of partitions based on the provided demoting plan.

        Args:
            demoting_plan (dict): A dictionary containing the demoting plan.

        Raises:
            ChangeReplicaAssignmentError: If an error occurs during the replica assignment change.

        Returns:
            None

        """
        demoting_plan_filepath = self._generate_tempfile_with_json_content(
            demoting_plan
        )
        command = "{}/bin/kafka-reassign-partitions.sh --bootstrap-server {} --reassignment-json-file {} --execute --timeout 60".format(
            self.kafka_path, self.bootstrap_servers, demoting_plan_filepath
        )
        env_vars = os.environ.copy()
        env_vars["KAFKA_HEAP_OPTS"] = self.kafka_heap_opts
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, env=env_vars
        )

        if result.returncode != 0:
            raise ChangeReplicaAssignmentError(result.stdout.strip())

    def _generate_tmpfile_with_admin_configs(self):
        """
        Generate a temporary file containing the admin configurations.

        If the temporary file doesn't already exist, it will be created. The admin configurations
        are written to the file, and the file is closed before returning its name.

        Returns:
            str: The path/name of the temporary file.

        """
        if self.admin_config_tmp_file is None:
            self.admin_config_tmp_file = tempfile.NamedTemporaryFile(delete=False)

        self.admin_config_tmp_file.write(self.admin_config_content.encode())
        self.admin_config_tmp_file.close()
        return self.admin_config_tmp_file.name

    def _trigger_leader_election(self, demoting_plan):
        """
        Trigger a leader election using the demoting plan.

        This method runs the `kafka-leader-election.sh` script with the provided demoting plan.
        The command is executed using the provided Kafka installation's path, the generated admin
        configurations, the bootstrap servers, and the path to the temporary file containing
        the demoting plan in JSON format.

        Args:
            demoting_plan (dict or list): A dictionary or list representation of the demoting plan.

        Raises:
            TriggerLeaderElectionError: If the leader election fails.

        """
        demoting_plan_filepath = self._generate_tempfile_with_json_content(
            demoting_plan
        )
        command = "{}/bin/kafka-leader-election.sh --admin.config {} --bootstrap-server {} --election-type PREFERRED --path-to-json-file {}".format(
            self.kafka_path,
            self._generate_tmpfile_with_admin_configs(),
            self.bootstrap_servers,
            demoting_plan_filepath,
        )
        env_vars = os.environ.copy()
        env_vars["KAFKA_HEAP_OPTS"] = self.kafka_heap_opts
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, env=env_vars
        )

        if result.returncode != 0:
            logger.error(
                "Failed to trigger leader election, error: {}, command: {}".format(
                    result.stdout.strip(), command
                )
            )
            raise TriggerLeaderElectionError(result.stdout.strip())

    def _save_rollback_plan(self, broker_id, current_partitions_state):
        logger.info("Saving rollback plan for broker {}".format(broker_id))
        self._produce_record(broker_id, current_partitions_state)
