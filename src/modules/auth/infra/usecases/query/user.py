from pydantic import EmailStr

from src.foundation.domain.value_objects import UUID
from src.modules.auth.app.repository.user import UserRepository
from src.modules.auth.app.usecases.dtos.user import UserOutputDto
from src.modules.auth.app.usecases.query.user import UserQuery as UserQueryBase
from src.modules.auth.domain.value_objects import UserID


class UserQuery(UserQueryBase):
    def __init__(self, repository: UserRepository):
        self._repository = repository

    def get_all(self, skip: int, limit: int) -> list[UserOutputDto]:
        return [
            UserOutputDto(
                id=UserID(user.id),
                username=user.username,
                email=EmailStr(user.email),
                first_name=user.first_name,
                last_name=user.last_name,
            )
            for user in self._repository.get_all_pagination(skip, limit)
        ]

    def get_by_id(self, id: UUID) -> UserOutputDto:
        user = self._repository.get_by_id(UserID(id))
        return UserOutputDto(**user.to_dict())
