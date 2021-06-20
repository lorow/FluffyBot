import abc


class AbstractConnector(abc.ABC):

    @abc.abstractmethod
    def connect(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def disconnect(self):
        raise NotImplementedError
