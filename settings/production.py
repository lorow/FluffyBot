import os
from .base import *


storage = {
    "base_redis": {
        "connection_details": {"url": os.environ.get("REDIS_URL", None)},
        "connector": "Core.repository.connectors.redis_connector.RedisConnector",
        "repositories": {
            "twitter_repository": "Core.repository.repositories.twitter_repository.TwitterRepository",
        },
    },
}