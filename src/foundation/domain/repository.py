from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from foundation.domain.entity import Entity


class GenericRepostirory(ABC):

    @abstractmethod
    def get_by_id(self, id: UUID):
        ...

    @abstractmethod
    def get_by_field_value(self, field: str, value: Any):
        ...

    @abstractmethod
    def update(self, entity: Entity):
        ...

    @abstractmethod
    def delete(self, id: UUID):
        ...

    @abstractmethod
    def create(self, entity: Any):
        ...

    @abstractmethod
    def exists(self, field: str, value: Any) -> bool:
        ...

    @abstractmethod
    def get_all(self):
        ...

    @abstractmethod
    def get_all_pagination(self, skip: int, limit: int):
        ...
