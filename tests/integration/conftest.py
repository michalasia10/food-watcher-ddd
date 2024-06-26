from typing import Any

import pytest
import pytest_asyncio

from src.config import settings
from src.modules.auth.application.dto import UserInputDto, UserAuthInputDto
from src.modules.auth.application.services import UserCrudService, AuthenticationService
from src.modules.auth.infra.user_repo import UserTortoiseRepo

from src.core.domain.repo.search_engine import ISearchRepository


class InMemorySearchRepository(ISearchRepository):
    """
    InMemorySearchRepository is a class that implements the ISearchRepository interface.
    """

    INDEX: str = ""
    SEARCH_FIELDS: list[str] | None = None
    FIELDS_TO_GET: list[str] | None = None

    def __init__(self, *args, **kwargs):
        self._documents: list[dict] = []

    async def asearch(
        self,
        query: str,
        offset: int = 0,
        limit: int = 100,
        fields_to_get: list[str] | None = None,
        search_fields: list[str] | None = None,
        *args,
        **kwargs,
    ) -> list[Any]:
        return filter(lambda document: query in document["id"], self._documents)

    async def aget_create_index(
        self,
        *args,
        **kwargs,
    ):
        raise NotImplementedError

    async def acreate_document(self, document: dict, *args, **kwargs) -> None:
        self._documents.append(document)

    async def adelete_document(self, document_id: str, *args, **kwargs) -> None:
        self._documents = list(
            filter(lambda document: document_id != document["id"], self._documents)
        )

    async def aupdate_document(
        self,
        document_id: str,
        document: dict,
        *args,
        **kwargs,
    ) -> None:
        for i, doc in enumerate(self._documents):
            if doc["id"] == document_id:
                self._documents[i] = document


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
            last_name="test",
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
            last_name="test2",
        )
    )


@pytest_asyncio.fixture(scope="function")
async def user_token(auth_service, user_password, user_record):
    return await auth_service.authenticate(
        UserAuthInputDto(username=user_record.username, password=user_password)
    )


@pytest_asyncio.fixture(scope="function")
async def user_token2(auth_service, user_password, user_record2):
    return await auth_service.authenticate(
        UserAuthInputDto(username=user_record2.username, password=user_password)
    )
