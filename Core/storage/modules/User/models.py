import sqlalchemy

from Core.storage.repository.model import SQLAlchemyModel


class UserModel(SQLAlchemyModel):
    __tablename__ = "discord_base_user"
    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
