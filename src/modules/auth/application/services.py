import time

import jwt
from tortoise.exceptions import DoesNotExist

from src.core.app.service import IAuthService, BaseCrudService
from src.modules.auth.application.dto import (
    UserInputDto,
    UserOutputDto,
    UserAuthInputDto,
    TokenOutputDto,
)
from src.modules.auth.domain.errors import (
    InvalidToken,
    BadCredentials,
    UserNotFound,
    UserNotRecordOwner,
)
from src.modules.auth.domain.user import User
from src.modules.auth.domain.user_repo import IUserRepo


class UserCrudService(BaseCrudService):
    OUTPUT_DTO = UserOutputDto
    NOT_RECORD_OWNER_ERROR = (
        UserNotRecordOwner,
        "You are not allowed to update user with {id} id.",
    )
    NOT_FOUND_ERROR = (UserNotFound, "User not found with {id} id.")
    DOES_NOT_EXIST_ERROR = DoesNotExist

    async def create(self, input_dto: UserInputDto, **kwargs) -> UserOutputDto:
        user = User.create(
            username=input_dto.username,
            password=input_dto.password,
            email=input_dto.email,
            first_name=input_dto.first_name,
            last_name=input_dto.last_name,
        )
        await self._repository.asave(user)
        return UserOutputDto(**user.snapshot)


class AuthenticationService(IAuthService):
    def __init__(
        self,
        user_repository: [IUserRepo],
        secret_key: str,
        algorithm: str,
    ):
        self._user_repository = user_repository
        self._secret_key = secret_key
        self._algorithm = algorithm

    async def authenticate(
        self, credentials: UserAuthInputDto
    ) -> TokenOutputDto | BadCredentials:
        """
        Authenticate user with given credentials.

        Args:
            credentials: UserAuthInputDto: User credentials.

        Returns: TokenOutputDto | BadCredentials

        """
        user: User = await self._user_repository.aget_first_from_filter(
            username=credentials.username
        )
        if not user:
            raise BadCredentials("User not found for given credentials.")

        if user.correct_password(credentials.password):
            return TokenOutputDto(
                api_token=user.create_token(
                    secret_key=self._secret_key, algorithm=self._algorithm
                ),
                user_id=user.id,
            )

        raise BadCredentials("Incorrect password.")

    @classmethod
    def _verify_time(cls, decoded_jwt: dict):
        """
        Verify if token is expired.

        Args:
            decoded_jwt: dict: Decoded JWT token.

        Returns: None | InvalidToken

        """
        expires = decoded_jwt.get("expires")
        if expires < time.time():
            raise InvalidToken("Token expired.")

    @classmethod
    def _decode_jwt(cls, secret_key: str, algorithm: str, credentials: str) -> dict:
        """
        Decode JWT token.

        Args:
            secret_key: str: Secret key.
            algorithm:  str: Algorithm.
            credentials: str: JWT token.

        Returns: dict

        """

        try:
            return jwt.decode(jwt=credentials, key=secret_key, algorithms=algorithm)
        except jwt.ExpiredSignatureError:
            raise InvalidToken("Token expired.")
        except jwt.InvalidTokenError:
            raise InvalidToken("Invalid token. Can't decode.")

    async def verify(self, token: str) -> User | BadCredentials:
        """
        Verify token and return user.

        Args:
            token: str: JWT token.

        Returns: User | BadCredentials

        """

        decoded_jwt = self._decode_jwt(
            secret_key=self._secret_key, algorithm=self._algorithm, credentials=token
        )
        self._verify_time(decoded_jwt)
        user: User | None = await self._user_repository.aget_first_from_filter(
            **User.get_user_filter_by_decoded_token(decoded_jwt)
        )

        if not user:
            raise BadCredentials("Invalid token, User not found.")

        return user
