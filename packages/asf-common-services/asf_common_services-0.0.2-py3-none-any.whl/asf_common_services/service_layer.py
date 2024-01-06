from asf_common_services.database.mongodb import MongoDBService
from asf_common_services.cache.redis_cache import RedisCacheService
from asf_common_services.messaging.kafka_messaging import KafkaMessagingService


class CommonServices:
    def __init__(self):
        self.mongo_service = MongoDBService()
        self.redis_service = RedisCacheService()
        self.kafka_service = KafkaMessagingService()

    # Methods abstracting the underlying services
    def insert_document(self, collection_name, document_data):
        return self.mongo_service.insert_document(collection_name, document_data)

    def get_document(self, collection_name, query):
        return self.mongo_service.get_document(collection_name, query)

    def set_cache(self, key, value):
        return self.redis_service.set(key, value)

    def get_cache(self, key):
        return self.redis_service.get(key)

    def send_message(self, topic, message):
        return self.kafka_service.send_message(topic, message)
