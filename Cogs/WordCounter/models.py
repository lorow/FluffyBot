import sqlalchemy

from Core.storage.repository.model import SQLAlchemyModel


class WordsToTrackModel(SQLAlchemyModel):
    __tablename__ = "doscord_discord_word_counter_tracted_words"
    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True, index=True
    )
    user = sqlalchemy.Column(sqlalchemy.ForeignKey("discord_base_user.id"))
    server = sqlalchemy.Column(sqlalchemy.String)
    word = sqlalchemy.Column(sqlalchemy.String)


class WordCounterModel(SQLAlchemyModel):
    __tablename__ = "discord_word_counter_word_count"
    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True, index=True
    )
    user = sqlalchemy.Column(sqlalchemy.ForeignKey("discord_base_user.id"))
    server = sqlalchemy.Column(sqlalchemy.String)
    word = sqlalchemy.Column(sqlalchemy.String)
    count = sqlalchemy.Column(sqlalchemy.Integer)
