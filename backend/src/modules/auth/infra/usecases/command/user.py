from typing import NoReturn

from src.modules.auth.app.repository.user import UserRepository
from src.modules.auth.app.usecases.command.user import UserCommand as UserCommandBase
from src.modules.auth.app.usecases.dtos.user import UserCreateInputDto
from src.modules.auth.domain.entities import User
from src.modules.auth.domain.exceptions import UserAlreadyExists, UserNotFound
from src.modules.auth.domain.value_objects import UserID


class UserCommand(UserCommandBase):
    def __init__(self, repository: UserRepository):
        self._repository = repository

    def create(self, user: UserCreateInputDto) -> NoReturn:
        if self._repository.exists('username', user.username):
            raise UserAlreadyExists('User already exists.')

        user = User(username=user.username, password=user.password, email=user.email)
        user.hash_pswd()

        self._repository.create(user)

    def delete(self, user_id: UserID):
        if not self._repository.exists('id', user_id):
            raise UserNotFound('User not found.')

        self._repository.delete(user_id)
