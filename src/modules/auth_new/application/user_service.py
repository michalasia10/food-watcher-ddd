import time
from uuid import UUID

import jwt
from tortoise.exceptions import DoesNotExist

from src.core_new.app.service import ICrudService, IAuthService
from src.modules.auth_new.application.dto import (
    UserInputDto,
    UserUpdateDto,
    UserOutputDto,
    UserAuthInputDto,
    TokenOutputDto
)
from src.modules.auth_new.domain.errors import InvalidToken, BadCredentials, UserNotFound, UserNotRecordOwner
from src.modules.auth_new.domain.user import User
from src.modules.auth_new.domain.user_repo import IUserRepo


class UserCrudService(ICrudService):
    def __init__(self, user_repository: [IUserRepo]):
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

    async def get(self, user_id: UUID) -> UserOutputDto:
        user = await self._user_repository.aget_by_id(user_id)
        return UserOutputDto(**user.snapshot)

    async def update(self, id: UUID, input_dto: UserUpdateDto, user_id: UUID = None, is_admin=False) -> UserOutputDto:
        if not is_admin and user_id != id:
            raise UserNotRecordOwner("You are not allowed to update this user.")

        user = await self._user_repository.aget_by_id(id)
        user.update(input_dto)
        await self._user_repository.aupdate(user)
        updated_user = await self._user_repository.aget_by_id(id)
        return UserOutputDto(**updated_user.snapshot)

    async def delete(self, id: UUID, user_id: UUID = None, is_admin=False) -> None:
        if not is_admin and user_id != id:
            raise UserNotRecordOwner("You are not allowed to delete this user.")

        user = await self.get_by_id(id)
        await self._user_repository.adelete(user)

    async def get_all(self, skip: int, limit: int) -> list[UserOutputDto]:
        users = await self._user_repository.aget_all(offset=skip, limit=limit)
        return [UserOutputDto(**user.snapshot) for user in users]

    async def get_by_id(self, id: UUID) -> UserOutputDto:
        try:
            user = await self._user_repository.aget_by_id(id)
        except  DoesNotExist:
            raise UserNotFound("User not found.")

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
            raise InvalidToken("Invalid token. Can't decode.")

    async def verify(self, token: str) -> User | BadCredentials:
        decoded_jwt = self._decode_jwt(
            secret_key=self._secret_key,
            algorithm=self._algorithm,
            credentials=token
        )
        self._verify_time(decoded_jwt)
        user: User | None = await (
            self._user_repository
            .aget_first_from_filter(**User.get_user_filter_by_decoded_token(decoded_jwt))
        )

        if not user:
            raise BadCredentials("Invalid token, User not found.")

        return user
