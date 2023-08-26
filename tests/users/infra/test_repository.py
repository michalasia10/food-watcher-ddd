import pytest
from src.modules.auth.domain.entities import User
from src.modules.auth.domain.value_objects import UserID
from src.modules.auth.infra.repository.user import SqlUserRepository
from tests.conftest import base_user_fix


def test_create_user_and_get(db_session):
    user = User(
        username="test",
        password="test",
    )
    repo = SqlUserRepository(db_session)
    repo.create(user)
    assert repo.get_by_id(UserID(user.id)) == user


def test_get_user_by_username(base_user_fix, db_session):
    repo = SqlUserRepository(db_session)
    assert repo.get_by_field_value("username", base_user_fix.username).username == base_user_fix.username
