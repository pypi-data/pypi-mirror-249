from kafka import KafkaProducer, KafkaConsumer, TopicPartition
from kafka.errors import KafkaError
from asf_common_services.service_config import KAFKA_CONFIG


class KafkaMessagingService:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.producer = KafkaProducer(**KAFKA_CONFIG)
            cls._instance.consumer = KafkaConsumer(**KAFKA_CONFIG)
        return cls._instance

    def send_message(self, topic, message):
        try:
            future = self.producer.send(topic, value=message.encode('utf-8'))
            result = future.get(timeout=10)  # Wait for acknowledgment
            return result.topic, result.partition, result.offset
        except KafkaError as e:
            print(f"Failed to send message: {e}")
            return None

    def consume_messages(self, topic):
        self.consumer.subscribe(topics=[topic])
        try:
            for message in self.consumer:
                yield message.value.decode('utf-8')
        except KeyboardInterrupt:
            self.consumer.close()

    def commit_offsets(self):
        self.consumer.commit()

    def seek_to_beginning(self, topic):
        partitions = self.consumer.partitions_for_topic(topic)
        if partitions is not None:
            for partition in partitions:
                self.consumer.seek_to_beginning({partition: 0})

    def seek_to_offset(self, topic, partition, offset):
        partitions = [TopicPartition(topic, partition)]
        self.consumer.assign(partitions)
        for partition in partitions:
            self.consumer.seek(partition, offset)

    def close_consumer(self):
        self.consumer.close()

    def close_producer(self):
        self.producer.flush()
        self.producer.close()
