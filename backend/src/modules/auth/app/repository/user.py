from abc import abstractmethod
from typing import Any, NoReturn

from foundation.domain.repository import GenericRepostirory
from modules.auth.domain.entities import User
from modules.auth.domain.value_objects import UserID


class UserRepository(GenericRepostirory):

    @abstractmethod
    def get_by_id(self, id: UserID) -> User:
        ...

    @abstractmethod
    def get_by_field_value(self, field: str, value: Any) -> User:
        ...

    @abstractmethod
    def update(self, entity: User) -> NoReturn:
        ...

    @abstractmethod
    def create(self, entity: User) -> NoReturn:
        ...
