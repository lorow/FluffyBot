import abc


class AbstractConnector(abc.ABC):
    def __init__(self, connection_details):
        self.connection_details = connection_details

    @abc.abstractmethod
    def connect(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def disconnect(self):
        raise NotImplementedError
