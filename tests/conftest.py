import asyncio
from enum import Enum

import pytest
import pytest_asyncio
from httpx import AsyncClient, BasicAuth
from tortoise import Tortoise

from src.api.main import app
from src.config import TORTOISE_TEST_CONFIG


@pytest.fixture(scope="function", autouse=True)
def endpoint_enum():
    class EndpointEnum(str, Enum):
        USERS = "/users/"
        AUTH = "/auth/"
        PRODUCTS = "/products/"
        CHAT = "/chat/"
        CONSUMPTION = "/consumption/"
        RECIPE = "/recipe/"

        def get_detail(self, id: int):
            return f"{self.value}{id}"

    return EndpointEnum


class AnsciColorEnum(str, Enum):
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    RESET = "\033[0m"


class LogLevelEnum(str, Enum):
    SETUP = "[SETUP-PYTEST]"
    TEARDOWN = "[TEARDOWN-PYTEST]"


class Printer:
    """
    Class to print messages with colors based on the log level.
    """

    @staticmethod
    def _printc(color: AnsciColorEnum, text: str, textt: str | None = None):
        """
        Base method to print colored text.
        """
        print(f"\n{color.value}{text}{AnsciColorEnum.RESET.value} {textt or ''}")

    @classmethod
    def _printl(cls, level: LogLevelEnum, text: str):
        """
        Print colored text based on the log level.
        """
        match level:
            case LogLevelEnum.SETUP.value:
                color = AnsciColorEnum.GREEN
            case LogLevelEnum.TEARDOWN.value:
                color = AnsciColorEnum.RED
            case _:
                color = AnsciColorEnum.YELLOW

        cls._printc(color, level.value, text)

    @classmethod
    def teardown(cls, text: str):
        """
        Print teardown message.

        e.g

        text: Dropping tables...
        ->>
        [TEARDOWN-PYTEST] Dropping tables...

        """
        cls._printl(LogLevelEnum.TEARDOWN, text)

    @classmethod
    def setup(cls, text: str):
        """
        Print setup message.

        e.g

        text: Creating tables...
        ->>
        [SETUP-PYTEST] Creating tables...

        """
        cls._printl(LogLevelEnum.SETUP, text)


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


class TestAsyncClient(AsyncClient):

    def set_token(self, token: str):
        self.headers = {
            "Authorization": f"Bearer {token}"
        }

    @staticmethod
    def check_correct_keys_in_error_response(response: dict) -> None:
        assert all(key in ["error", "status_code"] for key in response.keys())

    @staticmethod
    def check_status_code_in_error_response(response: dict, status_code: int) -> None:
        assert response["status_code"] == status_code


@pytest_asyncio.fixture(scope="function", autouse=True)
async def api_client():
    async with TestAsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="function", autouse=True)
def db(request, event_loop):
    async def _drop_db() -> None:
        # ToDO: Implement drop db
        Printer.teardown("Dropping tables...")
        conn = Tortoise.get_connection("default")
        try:
            drop_query = """DROP SCHEMA IF EXISTS PUBLIC CASCADE;"""
            await conn.execute_query(drop_query)

            Printer.teardown("All tables dropped successfully.")
        except Exception as e:
            Printer.teardown(f"Error dropping tables: {e}")
        finally:
            # Close the connection
            await conn.close()
            await Tortoise.close_connections()
            Printer.teardown("Connection closed.")

    def __drop():
        event_loop.run_until_complete(_drop_db())

    async def _init():
        Printer.setup("Creating tables...")
        await Tortoise.init(config=TORTOISE_TEST_CONFIG)
        conn = Tortoise.get_connection("default")
        create_schema_public = """CREATE SCHEMA IF NOT EXISTS PUBLIC;"""
        await conn.execute_query(create_schema_public)
        await Tortoise.generate_schemas(safe=True)
        Printer.setup("Tables created successfully.")

    event_loop.run_until_complete(_init())
    request.addfinalizer(__drop)
