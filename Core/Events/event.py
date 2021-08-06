import dataclasses


@dataclasses.dataclass
class BaseEvent:
    event_name: str
