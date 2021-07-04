import aioredis

from Core.repository.connector import AbstractConnector


class RedisConnector(AbstractConnector):
    """ Manages the connection to redis instance"""
    def __init__(self, connection_details: dict):
        self.connection_details = connection_details
        self.redis = None

    def connect(self):
        # noinspection PyUnresolvedReferences
        redis = aioredis.from_url(url=self.connection_details.get("url"))
        self.redis = redis
        return redis

    async def disconnect(self):
        await self.redis.close()
