from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic
from uuid import UUID as UUDIBase

from src.foundation.domain.entity import Entity as E

Entity = TypeVar("Entity", bound=E)
UUID = TypeVar("UUID", bound=UUDIBase)


class GenericRepository(ABC, Generic[Entity, UUID]):
    """An interface for a generic repository with CRUD operations"""

    @abstractmethod
    def get_by_id(self, id: UUID, raw=False): ...

    @abstractmethod
    def get_by_field_value(self, field: str, value: Any, raw=False): ...

    @abstractmethod
    def get_by_field_values(self, raw=False, **kwargs): ...

    @abstractmethod
    def update(self, entity: [Entity], raw=False): ...

    @abstractmethod
    def delete(self, id: UUID): ...

    @abstractmethod
    def create(self, entity: Any, raw=False): ...

    @abstractmethod
    def exists(self, field: str, value: Any) -> bool: ...

    @abstractmethod
    def get_all(self) -> list[Entity]: ...

    @abstractmethod
    def get_all_pagination(self, skip: int, limit: int, **kwargs) -> list[Entity]: ...
