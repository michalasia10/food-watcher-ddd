from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel
from uuid6 import uuid6

from src.core_new.domain.types import SnapShot


def convert_uuid_to_str(obj: Any) -> str | list[dict[str, Any]] | dict[str, Any]:
    if isinstance(obj, UUID):
        return str(obj)
    elif isinstance(obj, dict):
        return {key: convert_uuid_to_str(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_uuid_to_str(item) for item in obj]
    else:
        return obj


@dataclass
class Entity(ABC):
    id: UUID
    updated_at: datetime = field(kw_only=True)
    created_at: datetime = field(kw_only=True)

    def __eq__(self, other: 'Entity') -> bool:
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __str__(self):
        return f'.::{self.__class__.__name__}::..::{self.id}::.'

    @classmethod
    def create_id(cls) -> UUID:
        return uuid6()

    @property
    def snapshot(self) -> SnapShot:
        def filter(value):
            if isinstance(value, list):
                """
                check if value is empty list
                """
                return value if value else False

            """
            otherwise check if value is None
            """
            return value is not None

        _snapshot = asdict(self, dict_factory=lambda x: {k: v for (k, v) in x if filter(v)})
        return convert_uuid_to_str(_snapshot)

    @classmethod
    def create_now_time(cls) -> datetime:
        return datetime.now()

    @classmethod
    @abstractmethod
    def create(cls, *args, **kwargs) -> 'Entity':
        ...

    def update(self, input_dto: BaseModel) -> 'Entity':
        for _field, value in input_dto.dict().items():
            if getattr(self, _field) != value:
                setattr(self, _field, value)
        return self
