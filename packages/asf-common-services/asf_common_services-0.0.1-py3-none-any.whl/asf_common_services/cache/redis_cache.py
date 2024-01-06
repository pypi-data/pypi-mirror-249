import redis
from asf_common_services.service_config import REDIS_CONFIG


class RedisCacheService:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.client = redis.StrictRedis(**REDIS_CONFIG)
            cls._instance.pipeline = cls._instance.client.pipeline()
        return cls._instance

    def set(self, key, value):
        try:
            return self.client.set(key, value)
        except redis.RedisError as e:
            print(f"Failed to set value: {e}")
            return None

    def get(self, key):
        try:
            return self.client.get(key)
        except redis.RedisError as e:
            print(f"Failed to get value: {e}")
            return None

    def hset(self, key, field, value):
        try:
            return self.client.hset(key, field, value)
        except redis.RedisError as e:
            print(f"Failed to set hash value: {e}")
            return None

    def hget(self, key, field):
        try:
            return self.client.hget(key, field)
        except redis.RedisError as e:
            print(f"Failed to get hash value: {e}")
            return None

    def hgetall(self, key):
        try:
            return self.client.hgetall(key)
        except redis.RedisError as e:
            print(f"Failed to get all hash values: {e}")
            return None

    def hdel(self, key, *fields):
        try:
            return self.client.hdel(key, *fields)
        except redis.RedisError as e:
            print(f"Failed to delete hash fields: {e}")
            return None

    def pipeline_execute(self):
        try:
            return self.pipeline.execute()
        except redis.RedisError as e:
            print(f"Pipeline execution failed: {e}")
            return None

    def pipeline_reset(self):
        self.pipeline.reset()

    def pipeline_set(self, key, value):
        self.pipeline.set(key, value)

    def pipeline_get(self, key):
        self.pipeline.get(key)

    # Add pipeline support for other methods as needed
