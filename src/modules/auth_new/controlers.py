from classy_fastapi import post
from dependency_injector.wiring import inject

from api.shared import dependency
from config.di import ApiConfig
from src.core_new.controller.crud import BaseModelView
from src.modules.auth_new.application.dto import (
    UserAuthInputDto,
    TokenOutputDto,
    UserInputDto,
    UserOutputDto,
)
from src.modules.auth_new.application.user_service import AuthenticationService


class UserViewSet(BaseModelView[UserInputDto, UserOutputDto]):
    prefix = "/users"
    tag = "users"

    @inject
    def __init__(
            self,
            service=dependency(ApiConfig.auth.user_service),
            auth_service=dependency(ApiConfig.auth.auth_service),
    ) -> None:
        super(UserViewSet, self).__init__(
            service=service,
            auth_service=auth_service,
            create_dto=UserInputDto,
            output_dto=UserOutputDto,
        )

    @post("/login")
    @inject
    async def login(
            self,
            credentials: UserAuthInputDto,
            auth_service: AuthenticationService = dependency(ApiConfig.auth.user_service),
    ) -> TokenOutputDto:
        """Endpoint to authenticate user."""

        return await auth_service.authenticate(credentials)
