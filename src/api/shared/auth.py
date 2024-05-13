import time
from typing import Any, Union

import jwt
from dependency_injector.wiring import inject
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config.api_config import ApiConfig
from config.di import Container
from src.modules.auth.app.repository.user import UserRepository
from src.modules.auth.infra.models.user import User
from .dependency import dependency

http_bearer = HTTPBearer()


class JWTAUthBearer:
    # ToDo: refactor + move to auth

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def __call__(
        self, token: HTTPAuthorizationCredentials = Depends(http_bearer)
    ):
        if token:
            if not self.verify_time(token.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            if user := self.verify_user(token.credentials):
                return user
            raise HTTPException(status_code=403, detail="User not found for token.")

        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    @staticmethod
    def decode_jwt(token: str) -> dict | str:
        config = ApiConfig()
        try:
            return jwt.decode(token, config.SECRET_KEY, config.ALGORITHM)
        except jwt.ExpiredSignatureError:
            return "Token expired"
        except jwt.InvalidTokenError:
            return "Invalid token"

    def verify_user(self, token: str):
        user: Union[None, Any] = None
        try:
            decoded = self.decode_jwt(token)
            username = decoded["username"]
        except:
            username = None
        if username:
            user = self._user_repository.get_by_field_value("username", username)

        return user

    @classmethod
    def verify_time(cls, token: str):
        is_token_valid: bool = False
        try:
            decoded = cls.decode_jwt(token)
            payload = decoded if decoded["expires"] >= time.time() else None
        except:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid


@inject
async def bearer_auth(
    user_repository: UserRepository = dependency(Container.user_repository),
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> HTTPException | User:
    """Walk-around to use DI and Bearer."""

    _jwt = JWTAUthBearer(user_repository)
    return await _jwt(token)
