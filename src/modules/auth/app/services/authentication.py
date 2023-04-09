from abc import ABC,abstractmethod

from src.modules.auth.app.usecases.dtos import UserAuthInputDto, TokenOutputDto
from src.modules.auth.domain.exceptions import BadCredentials, UserNotFound


class AuthService(ABC):

    @abstractmethod
    def _create_token(self, credentials: UserAuthInputDto) -> TokenOutputDto:
        ...

    @abstractmethod
    def authenticate(self, credentials: UserAuthInputDto) -> TokenOutputDto | BadCredentials | UserNotFound:
        ...
