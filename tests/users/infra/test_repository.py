from src.modules.auth.domain.entities import User
from src.modules.auth.domain.value_objects import UserID
from src.modules.auth.infra.repository.user import SqlUserRepository
import pytest


@pytest.fixture
def base_user(db_session):
    repo = SqlUserRepository(db_session)

    user = User(
        username="test",
        password="test",
    )
    return repo.create(user)


def test_create_user_and_get(db_session):
    user = User(
        username="test",
        password="test",
    )
    repo = SqlUserRepository(db_session)
    repo.create(user)
    assert repo.get_by_id(UserID(user.id)) == user


def test_get_user_by_username(base_user, db_session):
    repo = SqlUserRepository(db_session)
    assert repo.get_by_field_value("username", base_user.username).username == base_user.username
