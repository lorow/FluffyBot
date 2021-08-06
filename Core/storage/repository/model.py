import abc
import dataclasses

from sqlalchemy.orm import declarative_base


@dataclasses.dataclass
class AbstractModel(abc.ABC):
    pass


SQLAlchemyModel = declarative_base()
