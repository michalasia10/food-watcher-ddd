from abc import ABC
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Any
from uuid import UUID

from uuid6 import uuid6

from core_new.domain.types import SnapShot


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
    updated_at: datetime = field(kw_only=True, default=None)
    created_at: datetime = field(kw_only=True, default=None)

    def __eq__(self, other: 'Entity') -> bool:
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    @classmethod
    def create_id(cls) -> UUID:
        return uuid6()

    @property
    def snapshot(self) -> SnapShot:
        _snapshot = asdict(self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None})
        return convert_uuid_to_str(_snapshot)
