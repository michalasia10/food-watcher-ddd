from classy_fastapi import post
from dependency_injector.wiring import inject
from fastapi import HTTPException, status

from api.routers.base import BaseModelView
from api.shared import dependency
from config.container_ioc import Container
from modules.auth.app.usecases.dtos import (
    UserAuthInputDto,
    TokenOutputDto,
    UserInputDto,
    UserOutputDto,
)
from src.api.shared.filters.validator import user_query_validator
from src.modules.auth.app.services.authentication import AuthService
from src.modules.auth.domain.exceptions import BadCredentials, UserNotFound


class UserViewSet(BaseModelView[UserInputDto, UserOutputDto]):
    prefix = "/users"
    tag = "users"

    @inject
    def __init__(
        self,
        query_service=dependency(Container.user_query),
        command_service=dependency(Container.user_command),
    ) -> None:
        super(UserViewSet, self).__init__(
            query_service=query_service,
            command_service=command_service,
            basic_create_dto=UserInputDto,
            basic_output_dto=UserOutputDto,
            filter_validator=user_query_validator,
        )

    @post("/login")
    @inject
    def login(
        self,
        credentials: UserAuthInputDto,
        auth_service: AuthService = dependency(Container.auth_service),
    ) -> TokenOutputDto:
        """Endpoint to authenticate user."""

        try:
            return auth_service.authenticate(credentials)
        except (UserNotFound, BadCredentials) as e:
            raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)
