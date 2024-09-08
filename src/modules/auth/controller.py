from uuid import UUID

from classy_fastapi import post, patch, get
from dependency_injector.wiring import inject
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.config.di import AppContainer
from src.core.app.service import IAuthService, ICrudService
from src.core.controller.crud import BaseModelView
from src.core.controller.di import dependency
from src.modules.auth.application.dto import (
    UserAuthInputDto,
    TokenOutputDto,
    UserInputDto,
    UserOutputDto,
    UserUpdateDto,
    UserSettingsDto,
)
from src.modules.auth.application.service.auth import AuthenticationService


class UserViewSet(BaseModelView[UserInputDto, UserOutputDto]):
    prefix = "/users"
    tag = "users"

    @inject
    def __init__(
        self,
        crud_service=dependency(AppContainer.auth.user_service),
        auth_service=dependency(AppContainer.auth.auth_service),
    ) -> None:
        super(UserViewSet, self).__init__(
            crud_service=crud_service,
            auth_service=auth_service,
            create_dto=UserInputDto,
            update_dto=UserUpdateDto,
            output_dto=UserOutputDto,
        )

    @post(
        path="/login",
        response_model=TokenOutputDto,
    )
    @inject
    async def login(
        self,
        credentials: UserAuthInputDto,
        auth_service: AuthenticationService = dependency(AppContainer.auth.auth_service),
    ) -> TokenOutputDto:
        """Endpoint to authenticate user."""

        return await auth_service.authenticate(credentials)

    @post(
        path="/refresh_token",
        response_model=TokenOutputDto,
    )
    @inject
    async def refresh_token(
        self,
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
        auth_service: IAuthService = dependency(AppContainer.auth.auth_service),
    ) -> TokenOutputDto:
        """Endpoint to refresh user token. User needs to be authenticated and remember to refresh token on time."""

        user = await auth_service.verify(token.credentials)

        return auth_service.refresh_token(user=user)

    @patch(path="/settings", response_model=UserSettingsDto)
    async def update_user_settings(
        self,
        settings: UserAuthInputDto,
        settings_service: ICrudService = dependency(AppContainer.auth.user_settings_service),
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
        auth_service: AuthenticationService = dependency(AppContainer.auth.auth_service),
    ):
        user = await auth_service.verify(token.credentials)

        return await settings_service.update(user_id=user.id, input_dto=settings, id=None)

    @get(path="/settings", response_model=UserSettingsDto)
    async def get_user_settings(
        self,
        id: UUID,
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
        auth_service: AuthenticationService = dependency(AppContainer.auth.auth_service),
        settings_service: ICrudService = dependency(AppContainer.auth.user_settings_service),
    ):
        user = await auth_service.verify(token.credentials)

        return await settings_service.get_by_user_id(user_id=user.id)
