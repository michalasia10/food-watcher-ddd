import uuid

import pytest
import pytest_asyncio

from src.config import settings
from src.modules.auth.application.dto import UserInputDto, UserAuthInputDto, TokenOutputDto
from src.modules.auth.application.services import UserCrudService, AuthenticationService
from src.modules.auth.infra.user_repo import UserTortoiseRepo


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


@pytest_asyncio.fixture(scope="function")
async def user_record2(user_service, user_password):
    return await user_service.create(
        UserInputDto(
            username="test2",
            password=user_password,
            email="test2@no.com",
            first_name="test2",
            last_name="test2"
        )
    )


@pytest_asyncio.fixture(scope="function")
async def user_token(auth_service, user_password, user_record):
    return await auth_service.authenticate(
        UserAuthInputDto(
            username=user_record.username,
            password=user_password
        )
    )


@pytest_asyncio.fixture(scope="function")
async def user_token2(auth_service, user_password, user_record2):
    return await auth_service.authenticate(
        UserAuthInputDto(
            username=user_record2.username,
            password=user_password
        )
    )


@pytest.fixture
def dummy_token():
    return TokenOutputDto(
        api_token=str(uuid.uuid4()),
        user_id=str(uuid.uuid4())
    )
