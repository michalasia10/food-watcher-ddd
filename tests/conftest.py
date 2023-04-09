import logging
import os
from contextvars import ContextVar

import pytest
from alembic import command
from alembic.config import Config

from src.api.main import CurrentUser
from src.config.api_config import ApiConfig
from src.config.container_ioc import create_configured_engine, create_request_context

disable_loggers = ['sqlalchemy.engine.Engine']


def pytest_configure():
    for logger_name in disable_loggers:
        logger = logging.getLogger(logger_name)
        logger.disabled = True


def pytest_sessionstart(session):
    config = Config(os.path.join('src', 'migrations', 'alembic.ini'))
    config.set_main_option('script_location', 'src/migrations')
    app_conf = ApiConfig()
    config.set_main_option('url', app_conf.TEST_DATABASE_URL)
    command.upgrade(config, 'head')


@pytest.fixture(scope='session')
def engine():
    return create_configured_engine({"DATABASE_URL": ApiConfig().TEST_DATABASE_URL, "DEBUG": True})


@pytest.fixture(scope='function')
def db_session(request, engine) -> ContextVar:
    session = create_request_context(engine)
    session.begin_request(CurrentUser.fake_user())

    def teardown():
        session.end_request()

    request.addfinalizer(teardown)
    return session.db_session


@pytest.fixture(scope="session", autouse=True)
def drop_db_after_tests(engine):
    yield
    with engine.connect() as conn:
        conn.execute("""SELECT 'DROP TABLE IF EXISTS "' || tablename || '" CASCADE;' 
                        from pg_tables WHERE schemaname = 'public';""")
