from tortoise.exceptions import DoesNotExist

from src.core.app.service import BaseCrudService
from src.core.domain.repo.postgres import IPostgresRepository
from src.core.domain.repo.search_engine import ISearchRepository
from src.modules.auth.application.dto import (
    UserInputDto,
    UserOutputDto,
)
from src.modules.auth.domain.entity.settings import UserSettings, Macro
from src.modules.auth.domain.entity.user import User
from src.modules.auth.domain.errors import (
    UserNotFound,
    UserNotRecordOwner,
)


class UserCrudService(BaseCrudService):
    OUTPUT_DTO = UserOutputDto
    NOT_RECORD_OWNER_ERROR = (
        UserNotRecordOwner,
        "You are not allowed to update user with {id} id.",
    )
    NOT_FOUND_ERROR = (UserNotFound, "User not found with {id} id.")
    DOES_NOT_EXIST_ERROR = DoesNotExist
    FETCH_FIELDS = [
        "settings",
        "settings__macro",
    ]

    def __init__(
        self,
        repository: [IPostgresRepository],
        settings_repository: [IPostgresRepository],
        macro_repository: [IPostgresRepository],
        search_repo: [ISearchRepository] = None,
    ):
        super().__init__(repository, search_repo)
        self._settings_repository = settings_repository
        self._macro_repository = macro_repository

    async def create(self, input_dto: UserInputDto, **kwargs) -> UserOutputDto:
        user = User.create(
            username=input_dto.username,
            password=input_dto.password,
            email=input_dto.email,
            first_name=input_dto.first_name,
            last_name=input_dto.last_name,
        )
        settings = UserSettings.create(
            user_id=user.id,
            age=input_dto.settings.age,
            gender=input_dto.settings.gender,
        )

        _macro = input_dto.settings.macro

        macro = Macro.create(
            settings_id=settings.id,
            fats=_macro.fats if _macro else None,
            proteins=_macro.proteins if _macro else None,
            gender=input_dto.settings.gender,
            carbs=_macro.carbs if _macro else None,
            calories=_macro.calories if _macro else None,
        )
        await self._repository.asave(user)
        await self._settings_repository.asave(settings)
        await self._macro_repository.asave(macro)

        settings.macro = macro
        user.settings = settings

        return UserOutputDto(**user.snapshot)
