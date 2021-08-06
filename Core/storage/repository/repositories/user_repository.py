from Core.storage.modules.User.models import UserModel
from Core.storage.repository.repository import AbstractRepository


class UserRepository(AbstractRepository):
    def add(self, instance: UserModel):
        pass

    def get(self, reference) -> UserModel:
        pass

    def remove(self, reference):
        pass

    def update(self, reference, instance: UserModel) -> (bool, UserModel):
        pass
