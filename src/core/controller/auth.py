from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.core.app.service import IAuthService

http_bearer = HTTPBearer()


class AuthController:
    def __init__(self, auth_service: IAuthService):
        self._auth_service = auth_service

    async def bearer_auth(self, token: HTTPAuthorizationCredentials = Depends(http_bearer)):
        return await self._auth_service.verify(token.credentials)
