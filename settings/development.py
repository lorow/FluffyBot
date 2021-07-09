from .base import *

storage = {
    "base_redis": {
        "connection_details": {"url": "redis://localhost"},
        "connector": "Core.repository.connectors.redis_connector.RedisConnector",
        "repositories": {
            "twitter_repository": "Core.repository.repositories.twitter_repository.TwitterRepository",
        },
    },
}