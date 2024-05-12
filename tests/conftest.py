import asyncio

import pytest
from httpx import AsyncClient
from tortoise import Tortoise
from tortoise.backends.asyncpg.schema_generator import AsyncpgSchemaGenerator

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


@pytest.fixture(scope="function", autouse=True)
def db(request, event_loop):
    async def _drop_db() -> None:
        # ToDO: Implement drop db
        print("\n [TEARDOWN-PYTEST] Dropping tables...")
        conn = Tortoise.get_connection("default")
        try:
            drop_query = """DROP SCHEMA IF EXISTS PUBLIC CASCADE;"""
            await conn.execute_query(drop_query)

            print("\n [TEARDOWN-PYTEST] All tables dropped successfully.")
        except Exception as e:
            print(f"\n [TEARDOWN-PYTEST] Error dropping tables: {e}")
        finally:
            # Close the connection
            await conn.close()
            await Tortoise.close_connections()

    def __drop():
        event_loop.run_until_complete(_drop_db())

    async def _init():
        print("\n [SETUP-PYTEST] Creating tables...")
        await Tortoise.init(config=TORTOISE_TEST_CONFIG)
        conn = Tortoise.get_connection("default")
        create_schema_public = """CREATE SCHEMA IF NOT EXISTS PUBLIC;"""
        await conn.execute_query(create_schema_public)
        await Tortoise.generate_schemas(safe=True)
        print("\n [SETUP-PYTEST] Tables created successfully.")

    event_loop.run_until_complete(_init())
    request.addfinalizer(__drop)
