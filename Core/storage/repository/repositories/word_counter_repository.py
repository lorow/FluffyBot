from Core.storage.repository import model
from Core.storage.repository.repository import AbstractRepository


class WordCounterRepository(AbstractRepository):
    def add(self, instance: model.AbstractModel):
        pass

    def get(self, word: str, for_user: str = None) -> model.AbstractModel:
        pass

    def remove(self, reference):
        pass

    def update(
        self, reference, instance: model.AbstractModel
    ) -> (bool, model.AbstractModel):
        pass
