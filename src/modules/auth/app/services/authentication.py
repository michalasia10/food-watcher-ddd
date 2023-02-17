from abc import ABC,abstractmethod

from modules.auth.app.usecases.dtos import UserAuthInputDto, TokenOutputDto
from modules.auth.domain.exceptions import BadCredentials, UserNotFound


class AuthService(ABC):

    @abstractmethod
    def _create_token(self, credentials: UserAuthInputDto) -> TokenOutputDto:
        ...

    @abstractmethod
    def authenticate(self, credentials: UserAuthInputDto) -> TokenOutputDto | BadCredentials | UserNotFound:
        ...
