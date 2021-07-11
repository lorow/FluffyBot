import os
from .base import *


database_url = os.environ.get("DATABASE_URL", None)
# make the url compatible with sqlalchemy
if database_url:
    database_url = database_url.replace("postgres://", "postgresql+asyncpg://")

storage = {
    "base_redis": {
        "connection_details": {"url": os.environ.get("REDIS_URL", None)},
        "connector": "Core.repository.connectors.redis_connector.RedisConnector",
        "repositories": {
            "twitter_repository": "Core.repository.repositories.twitter_repository.TwitterRepository",
        },
    },
    "base_postgresql": {
        "connection_details": {"url": database_url},
        "connector": "Core.repository.connectors.postgresql_connector.PostgresqlConnector",
        "repositories": {
            "user_repository": "Core.repository.repositories.user_repository.UserRepository",
            "word_counter_repository": "Core.repository.repositories.word_counter_repository.WordCounterRepository",
        }
    }
}

