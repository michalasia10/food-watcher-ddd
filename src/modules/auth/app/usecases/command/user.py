from abc import abstractmethod
from typing import NoReturn

from foundation.application.commands import CommandBase
from src.modules.auth.app.usecases.dtos.user import UserInputDto, UserOutputDto
from src.modules.auth.domain.value_objects import UserID


class UserCommand(CommandBase):

    @abstractmethod
    def create(self, user: UserInputDto) -> NoReturn:
        ...

    @abstractmethod
    def delete(self, id: UserID):
        ...

    @abstractmethod
    def update(self, id: UserID, user: UserInputDto) -> UserOutputDto:
        ...
