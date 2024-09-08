from dependency_injector import containers, providers

from src.modules.auth.application.service.auth import AuthenticationService
from src.modules.auth.application.service.user import UserCrudService
from src.modules.auth.application.service.settings import UserSettingsService
from src.modules.auth.infra.repo.settings import (
    UserSettingsTortoiseRepo,
    MacroTortoiseRepo,
)
from src.modules.auth.infra.repo.user import UserTortoiseRepo


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
        settings_repository=UserSettingsTortoiseRepo,
        macro_repository=MacroTortoiseRepo,
    )
    user_settings_service = providers.Factory(
        UserSettingsService,
        settings_repository=UserSettingsTortoiseRepo,
        macro_repository=MacroTortoiseRepo,
    )
