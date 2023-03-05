import dataclasses
from typing import NoReturn

from src.modules.auth.app.repository.user import UserRepository
from src.modules.auth.app.usecases.command.user import UserCommand as UserCommandBase
from src.modules.auth.app.usecases.dtos.user import UserInputDto, UserOutputDto
from src.modules.auth.domain.entities import User
from src.modules.auth.domain.exceptions import UserAlreadyExists, UserNotFound
from src.modules.auth.domain.value_objects import UserID


class UserCommand(UserCommandBase):
    def __init__(self, repository: UserRepository):
        self._repository = repository

    def create(self, user: UserInputDto) -> UserOutputDto:
        if self._repository.exists('username', user.username):
            raise UserAlreadyExists('User already exists.')
        user = self._repository.create(User(**dataclasses.asdict(user)))

        return UserOutputDto(id=user.id,
                             username=user.username,
                             email=user.email,
                             first_name=user.first_name,
                             last_name=user.last_name)

    def delete(self, id: UserID):
        if not self._repository.exists('id', id):
            raise UserNotFound('User not found.')

        self._repository.delete(id)

    def update(self, id: UserID, user: UserInputDto) -> UserOutputDto:
        return self._repository.update(User(**dataclasses.asdict(user)))
