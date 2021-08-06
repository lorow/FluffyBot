import sqlalchemy

from Core.repository.model import SQLAlchemyModel


class WordCounterModel(SQLAlchemyModel):
    __tablename__ = "discord_word_counter"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user = sqlalchemy.Column(sqlalchemy.ForeignKey("discord_base_user.id"))
    word = sqlalchemy.Column(sqlalchemy.String)
    count = sqlalchemy.Column(sqlalchemy.Integer)
