import uuid
from dataclasses import dataclass

from Core.storage.repository.model import AbstractModel


@dataclass
class KCUTweet(AbstractModel):

    id: uuid
    tweet: str
    proposing_user: str
    has_been_posted: bool


@dataclass
class KCUStory(AbstractModel):

    id: uuid
    KCUTweet: uuid
    text: str
    vote_count: int = 0
