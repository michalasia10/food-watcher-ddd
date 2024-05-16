from classy_fastapi import post
from dependency_injector.wiring import inject

from src.api.shared import dependency
from src.config.di import AppContainer
from src.core_new.controller.crud import BaseModelView
from src.modules.auth_new.application.dto import (
    UserAuthInputDto,
    TokenOutputDto,
    UserInputDto,
    UserOutputDto,
    UserUpdateDto
)
from src.modules.auth_new.application.user_service import AuthenticationService


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