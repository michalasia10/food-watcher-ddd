from abc import ABC, abstractmethod
from typing import NoReturn

from src.modules.auth.app.usecases.dtos.user import UserCreateInputDto
from src.modules.auth.domain.value_objects import UserID


class UserCommand(ABC):

    @abstractmethod
    def create(self, user: UserCreateInputDto) -> NoReturn:
        ...

    @abstractmethod
    def delete(self, user_id: UserID):
        ...
