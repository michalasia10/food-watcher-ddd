import pytest

from src.modules.auth_new.application.dto import UserInputDto
from src.modules.auth_new.application.user_service import UserCrudService
from src.modules.auth_new.infra.user_repo import UserTortoiseRepo


@pytest.fixture
def user_service():
    return UserCrudService(UserTortoiseRepo)


@pytest.fixture
def user_repo():
    return UserTortoiseRepo


@pytest.fixture
async def user_record(user_service):
    return await user_service.create(
        UserInputDto(
            username="test",
            password="test",
            email="test@no.com",
            first_name="test",
            last_name="test"
        )
    )
