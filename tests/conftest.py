import contextlib
import logging
import os
from contextvars import ContextVar

import pytest
from alembic import command
from alembic.config import Config

from src.modules.products.infra.models.product import Product
from src.foundation.infra.db import metadata
from src.api.main import CurrentUser
from src.config.api_config import ApiConfig
from src.config.container_ioc import create_configured_engine, create_request_context
from src.modules.auth.domain.entities import User
from src.modules.auth.infra.repository.user import SqlUserRepository
from src.modules.products.infra.repository.product import (
    SqlProductRepository,
    SqlDailyUserProductRepository,
    SqlDailyUserConsumptionRepository
)
from src.modules.recipes.infra.repository.recipe import SqlRecipeRepository, SqlRecipeProductRepository

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


def drop_db_after_tests(engine):
    with contextlib.closing(engine.connect()) as con:
        trans = con.begin()
        print("\n" + "#" * 25 + f" Number of {len(metadata.sorted_tables)} tables to delete" + "#" * 25 + "\n")
        for table in reversed(metadata.sorted_tables):
            con.execute(table.delete())
        trans.commit()
    print("\n" + "#" * 25 + " Dropped tables after test" + "#" * 25 + "\n")


@pytest.fixture(scope='function')
def db_session(request, engine) -> ContextVar:
    session = create_request_context(engine)
    session.begin_request(CurrentUser.fake_user())

    def teardown():
        session.end_request()
        drop_db_after_tests(engine)
        session.db_session.get().close()

    request.addfinalizer(teardown)
    return session.db_session


@pytest.fixture
def base_user_fix(db_session):
    repo = SqlUserRepository(db_session)

    user = User(
        username="test",
        password="test",
    )
    _user = repo.create(user)
    repo.commit()
    return _user


@pytest.fixture(autouse=True)
def product_repo(db_session):
    return SqlProductRepository(db_session=db_session)


@pytest.fixture(autouse=True)
def daily_user_product_repo(db_session):
    return SqlDailyUserProductRepository(db_session=db_session)


@pytest.fixture(autouse=True)
def daily_user_consumption_repo(db_session):
    return SqlDailyUserConsumptionRepository(db_session=db_session)


@pytest.fixture(autouse=True)
def recipe_repo(db_session):
    return SqlRecipeRepository(db_session=db_session)

@pytest.fixture(autouse=True)
def recipe_product_repo(db_session):
    return SqlRecipeProductRepository(db_session=db_session)

@pytest.fixture
def product_fix(product_repo):
    product = Product(
        code=28001461,
        name="test",
        quantity="250g",
        brand="Test",
        size="test",
        fat_100g=10.0,
        carbohydrates_100g=10.0,
        sugars_100g=10.0,
        proteins_100g=10.0,
        groups="tests",
        category="tests",
        energy_kcal_100g=10.0
    )
    return product_repo.create(product)

def commit_repos(repos):
    for repo in repos:
        repo.commit()
