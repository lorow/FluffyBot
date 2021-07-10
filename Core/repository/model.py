import abc

from sqlalchemy.orm import declarative_base


class AbstractModel(abc.ABC):
    pass

SQLAlchemyBase = declarative_base()

class SQLAlchemyModel(AbstractModel, SQLAlchemyBase):
    pass