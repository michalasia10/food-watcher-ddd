from pydantic import EmailStr

from src.modules.auth.app.repository.user import UserRepository
from src.modules.auth.app.usecases.dtos.user import UserOutputDto
from src.modules.auth.app.usecases.query.user import UserQuery as UserQueryBase


class UserQuery(UserQueryBase):
    def __init__(self, repository: UserRepository):
        self._repository = repository

    def get_all(self) -> list[UserOutputDto]:
        return [UserOutputDto(username=user.username,
                              email=EmailStr(user.email),
                              first_name=user.first_name,
                              last_name=user.last_name)
                for user in self._repository.get_all()]
