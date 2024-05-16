import pytest

from src.core_new.infra.tortoiserepo import TortoiseRepo
from src.modules.auth_new.application.dto import UserInputDto, UserUpdateDto
from src.modules.auth_new.application.user_service import UserCrudService


@pytest.mark.asyncio
async def test_user_service_create_user(user_service: UserCrudService, user_repo: TortoiseRepo):
    user_dto = UserInputDto(
        username="test",
        password="test",
        email="test@sth.com",
        first_name="test",
        last_name="test"
    )
    user = await user_service.create(user_dto)
    user_from_db = await user_repo.aget_by_id(user.id)

    for key, value in user_dto.dict().items():
        if key == "password":
            continue

        assert getattr(user_from_db, key) == value


@pytest.mark.asyncio
async def test_user_service_update_user(user_service: UserCrudService, user_repo: TortoiseRepo, user_record):
    u = await user_record
    user_dto = UserUpdateDto(email="sth@a.com")
    user = await user_service.update(u.id, user_dto)
    user_from_db = await user_repo.aget_by_id(user.id)
    assert user_from_db.email == user_dto.email
