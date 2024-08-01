from typing import Optional

from uuid6 import UUID
from src.core.app.service import ICrudService
from src.core.domain.value_object import PrecisedFloat
from src.core.domain.errors import NotSupportedError
from src.core.domain.repo.postgres import IPostgresRepository
from src.modules.auth.application.dto import UserSettingsDto, UserSettingsUpdateDto
from src.modules.auth.domain.entity.settings import Macro, UserSettings
from src.modules.auth.domain.errors import (
    UserSettingsNotFound,
)


class UserSettingsService(ICrudService):
    def __init__(
        self,
        settings_repository: IPostgresRepository,
        macro_repository: IPostgresRepository,
    ) -> None:
        self._settings_repository = settings_repository
        self._macro_repository = macro_repository

    async def create(self, *args, **kwargs) -> NotSupportedError:
        raise NotSupportedError(message="User can't create settings by himself")

    async def delete(self, *args, **kwargs) -> NotSupportedError:
        raise NotSupportedError(message="User can't delete settings by himself")

    async def update(
        self, input_dto: UserSettingsUpdateDto, user_id: Optional[UUID], id: UUID = None, is_admin: bool = False
    ) -> UserSettingsDto:
        settings: UserSettings = await self._settings_repository.aget_first_from_filter(user_id=user_id)

        if settings is None:
            raise UserSettingsNotFound(message="User settings not found.")

        macro: Macro = await self._macro_repository.aget_first_from_filter(settings_id=settings.id)

        if input_dto.gender:
            settings.gender = input_dto.gender

        if input_dto.age:
            settings.age = input_dto.age

        if input_dto.macro:
            _macro = input_dto.macro

            macro.fats = PrecisedFloat(_macro.fats)
            macro.proteins = PrecisedFloat(_macro.proteins)
            macro.calories = PrecisedFloat(_macro.calories)
            macro.carbs = PrecisedFloat(_macro.carbs)

            await self._macro_repository.aupdate(entity=macro)

        await self._settings_repository.aupdate(entity=settings)

        settings.macro = macro

        return UserSettingsDto(**settings.snapshot)

    async def get_all(
        self,
        skip: int,
        limit: int,
        query: str | None = None,
    ):
        raise NotSupportedError(message="Not supported `get all` for seetings")

    async def get_by_id(self, id: UUID):
        raise NotSupportedError(message="Not supported `get_by_id` for user seetings")

    async def get_by_user_id(self, user_id: UUID):
        settings = await self._settings_repository.aget_first_from_filter(user_id=user_id, fetch_fields=["macro"])

        return UserSettingsDto(**self._settings_repository.convert_snapshot(settings.snapshot))
