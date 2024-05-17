import pytest

from src.modules.auth_new.application.dto import UserInputDto
from src.modules.auth_new.application.user_service import UserCrudService, AuthenticationService
from src.modules.auth_new.infra.user_repo import UserTortoiseRepo


@pytest.fixture
def user_service():
    return UserCrudService(user_repository=UserTortoiseRepo)


@pytest.fixture
def auth_service():
    return AuthenticationService(
        user_repository=UserTortoiseRepo,
        secret_key="test",
        algorithm="HS256",
    )


@pytest.fixture
def user_repo():
    return UserTortoiseRepo


@pytest.fixture
def user_password():
    return "test_password"


@pytest.fixture
async def user_record(user_service, user_password):
    return await user_service.create(
        UserInputDto(
            username="test",
            password=user_password,
            email="test@no.com",
            first_name="test",
            last_name="test"
        )
    )
