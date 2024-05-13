import time

import jwt

from src.core_new.app.service import ICrudService, IAuthService
from src.modules.auth_new.application.dto import UserInputDto, UserOutputDto, UserAuthInputDto, TokenOutputDto
from src.modules.auth_new.domain.errors import InvalidToken, BadCredentials, UserNotFound
from src.modules.auth_new.domain.user import User
from src.modules.auth_new.domain.user_repo import IUserRepo


class UserCrudService(ICrudService):
    def __init__(self, user_repository: IUserRepo):
        self._user_repository = user_repository

    async def create(self, input_dto: UserInputDto) -> UserOutputDto:
        user = User.create(
            username=input_dto.username,
            password=input_dto.password,
            email=input_dto.email,
            first_name=input_dto.first_name,
            last_name=input_dto.last_name
        )
        await self._user_repository.asave(user)

        return UserOutputDto(**user.snapshot)


class AuthenticationService(IAuthService):
    def __init__(
            self,
            user_repository: IUserRepo,
            secret_key: str,
            algorithm: str,
    ):
        self._user_repository = user_repository
        self._secret_key = secret_key
        self._algorithm = algorithm

    async def authenticate(
            self,
            credentials: UserAuthInputDto
    ) -> TokenOutputDto | BadCredentials | UserNotFound:

        user: User = await self._user_repository.aget_first_from_filter(
            username=credentials.username
        )
        if not user:
            raise UserNotFound("User not found.")

        if user.correct_password(credentials.password):
            return TokenOutputDto(
                api_token=user.create_token(
                    secret_key=self._secret_key,
                    algorithm=self._algorithm
                ),
                user_id=user.id
            )

        raise BadCredentials("Incorrect password.")

    @classmethod
    def _verify_time(cls, decoded_jwt: dict):
        expires = decoded_jwt.get("expires")
        if expires < time.time():
            raise InvalidToken("Token expired.")

    @classmethod
    def _decode_jwt(
            cls,
            secret_key: str,
            algorithm: str,
            credentials: str
    ) -> dict:
        try:
            return jwt.decode(
                jwt=credentials,
                key=secret_key,
                algorithms=algorithm
            )
        except jwt.ExpiredSignatureError:
            raise InvalidToken("Token expired.")
        except jwt.InvalidTokenError:
            raise InvalidToken("Invalid token.")

    async def verify(self, token: str) -> User | BadCredentials:
        decoded_jwt = self._decode_jwt(
            secret_key=self._secret_key,
            algorithm=self._algorithm,
            credentials=token
        )
        self._verify_time(decoded_jwt)
        user: User | None = await self._user_repository.aget_first_from_filter(id=decoded_jwt.get("username"))

        if not user:
            BadCredentials("User not found.")

        return user
