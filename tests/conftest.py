import asyncio

import pytest
from httpx import AsyncClient
from tortoise import Tortoise

from src.api.main import app
from src.config import TORTOISE_TEST_CONFIG

DB_URL = "sqlite://:memory:"


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        print("Client is ready")
        yield client


@pytest.fixture(scope="session", autouse=True)
def db(request, event_loop):
    async def _drop_db() -> None:
        # ToDO: Implement drop db
        pass

    def __drop():
        event_loop.run_until_complete(_drop_db())

    async def _init():
        await Tortoise.init(config=TORTOISE_TEST_CONFIG)
        await Tortoise.generate_schemas(safe=True)

    event_loop.run_until_complete(_init())
    request.addfinalizer(__drop)
