from .base import *

storage = {
    "base_redis": {
        "connection_details": {"url": "redis://localhost"},
        "connector": "Core.repository.connectors.redis_connector.RedisConnector",
        "repositories": {
            "twitter_repository": "Core.repository.repositories.twitter_repository.TwitterRepository",
        },
    },
    "base_postgresql": {
        "connection_details": {"url": "mysql+aiomysql://lorow:password@localhost/fluffydev"},
        "connector": "Core.repository.connectors.postgresql_connector.PostgresqlConnector",
        "repositories": {
            "user_repository": "Core.repository.repositories.user_repository.UserRepository",
            "word_counter_repository": "Core.repository.repositories.word_counter_repository.WordCounterRepository",
        }
    }
}