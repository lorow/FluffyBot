import abc

from sqlalchemy.orm import declarative_base


class AbstractModel(abc.ABC):
    pass

SQLAlchemyModel = declarative_base()
