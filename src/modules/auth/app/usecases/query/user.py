from abc import ABC, abstractmethod

from src.modules.auth.app.usecases.dtos.user import UserOutputDto


class UserQuery(ABC):

    @abstractmethod
    def get_all(self) -> list[UserOutputDto]:
        ...
