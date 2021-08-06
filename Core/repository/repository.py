import abc

from Core.repository import model


class AbstractRepository(abc.ABC):
    def __init__(self, session):
        self.session = session

    @abc.abstractmethod
    def add(self, instance: model.AbstractModel):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> model.AbstractModel:
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, reference):
        raise NotImplementedError

    @abc.abstractmethod
    def update(
        self, reference, instance: model.AbstractModel
    ) -> (bool, model.AbstractModel):
        raise NotImplementedError
