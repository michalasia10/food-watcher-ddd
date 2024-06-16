from dependency_injector import containers, providers

from src.modules.auth.application.services import AuthenticationService, UserCrudService
from src.modules.auth.infra.user_repo import UserTortoiseRepo


class AuthContainer(containers.DeclarativeContainer):
    container_config = providers.Configuration()
    api_config = providers.ItemGetter()

    auth_service = providers.Factory(
        AuthenticationService,
        user_repository=UserTortoiseRepo,
        secret_key=api_config.SECRET_KEY,
        algorithm=api_config.ALGORITHM,
    )

    user_service = providers.Factory(
        UserCrudService,
        repository=UserTortoiseRepo,
    )
