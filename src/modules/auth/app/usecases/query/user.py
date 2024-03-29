from abc import abstractmethod

from src.foundation.application.queries import QueryBase
from src.foundation.domain.value_objects import UUID
from src.modules.auth.app.usecases.dtos.user import UserOutputDto


class UserQuery(QueryBase):

    @abstractmethod
    def get_all(self, skip: int, limit: int) -> list[UserOutputDto]:
        ...

    @abstractmethod
    def get_by_id(self, id: UUID) -> UserOutputDto:
        ...
