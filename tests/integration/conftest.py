import pytest
import pytest_asyncio

from src.config import settings
from src.modules.auth_new.application.dto import UserInputDto
from src.modules.auth_new.application.services import UserCrudService, AuthenticationService
from src.modules.auth_new.infra.user_repo import UserTortoiseRepo


@pytest.fixture
def user_service():
    return UserCrudService(repository=UserTortoiseRepo)


@pytest.fixture
def secret_key():
    return settings.SECRET_KEY


@pytest.fixture
def algorithm():
    return settings.ALGORITHM


@pytest.fixture
def auth_service(secret_key, algorithm):
    return AuthenticationService(
        user_repository=UserTortoiseRepo,
        secret_key=secret_key,
        algorithm=algorithm,
    )


@pytest.fixture
def user_repo():
    return UserTortoiseRepo


@pytest.fixture
def user_password():
    return "test_password"


@pytest_asyncio.fixture(scope="function")
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
