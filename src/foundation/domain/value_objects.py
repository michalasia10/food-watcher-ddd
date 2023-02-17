import uuid

from pydantic.dataclasses import dataclass

UUID = uuid.UUID
UUID.v4 = uuid.uuid4


@dataclass
class ValueObject:
    """
    Base class for value objects
    """
