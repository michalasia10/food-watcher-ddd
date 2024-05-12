from abc import abstractmethod
from typing import Any, NoReturn

from src.foundation.domain.repository import GenericRepository
from src.modules.auth.domain.entities import User
from src.modules.auth.domain.value_objects import UserID


class UserRepository(GenericRepository):

    @abstractmethod
    def get_by_id(self, id: UserID) -> User: ...

    @abstractmethod
    def get_by_field_value(self, field: str, value: Any) -> User: ...

    @abstractmethod
    def update(self, entity: User) -> NoReturn: ...

    @abstractmethod
    def create(self, entity: User) -> NoReturn: ...

    @abstractmethod
    def get_all(self) -> list[User]: ...

    @abstractmethod
    def get_all_pagination(self, skip: int, limit: int) -> list[User]: ...
