import time

import jwt
from sqlalchemy.exc import NoResultFound

from src.foundation.utils.functional import hash_helper
from src.modules.auth.app.repository.user import UserRepository
from src.modules.auth.app.services.authentication import AuthService
from src.modules.auth.app.usecases.dtos import TokenOutputDto
from src.modules.auth.app.usecases.dtos import UserAuthInputDto
from src.modules.auth.domain.entities import User
from src.modules.auth.domain.exceptions import BadCredentials, UserNotFound


class AuthenticationService(AuthService):

    def __init__(self, user_repository: UserRepository, secret_key: str, algorithm: str):
        self._user_repository = user_repository
        self._algorithm = algorithm
        self._secret_key = secret_key

    def _create_token(self, credentials: UserAuthInputDto) -> TokenOutputDto:
        payload = {
            'username': credentials.username,
            'expires': time.time() + 2400,
        }
        return TokenOutputDto(jwt.encode(payload, self._secret_key, self._algorithm))

    def authenticate(self, credentials: UserAuthInputDto) -> TokenOutputDto | BadCredentials | UserNotFound:
        try:
            user: User = self._user_repository.get_by_field_value('username', credentials.username)
        except NoResultFound:
            raise UserNotFound('User not found.')

        correct_password = hash_helper.verify(
            credentials.password, user.password
        )
        if correct_password:
            return self._create_token(credentials)

        raise BadCredentials("Incorrect password.")
