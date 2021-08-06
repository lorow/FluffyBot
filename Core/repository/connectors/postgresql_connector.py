from sqlalchemy.orm import sessionmaker

from Core.repository.connector import AbstractConnector

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


class PostgresqlConnector(AbstractConnector):
    """Manages the connection to async postgresql database"""

    def __init__(self, connection_details):
        super().__init__(connection_details)
        self.session = None

    def connect(self):
        engine = create_async_engine(self.connection_details.get("url"))
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        self.session = async_session
        return async_session

    async def disconnect(self):
        # todo handle graceful closing of sessions
        pass
