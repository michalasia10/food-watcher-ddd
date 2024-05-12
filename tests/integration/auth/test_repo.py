import pytest

from src.modules.auth_new.domain.enums import StatusEnum, TypeEnum
from src.modules.auth_new.domain.user import User
from src.modules.auth_new.infra.user_repo import UserTortoiseRepo


@pytest.mark.asyncio
async def test_create_and_get_client(db):
    # given
    email = "test@domain.com"
    user_to_create = User.create(
        email=email,
        password="test",
        username="test",
        first_name="test",
        last_name="test",
        status=StatusEnum.ACTIVE.value,
        type=TypeEnum.USER.value
    )
    await UserTortoiseRepo.asave(
        entity=user_to_create
    )

    # when
    user_get_from_db = await UserTortoiseRepo.aget_first_from_filter(email=email)

    # then
    assert user_get_from_db.email == user_to_create.email
    assert user_get_from_db.email == email
    assert user_get_from_db.username == user_to_create.username
    assert user_get_from_db.first_name == user_to_create.first_name
    assert user_get_from_db.created_at is not None
    assert user_get_from_db.updated_at is not None
