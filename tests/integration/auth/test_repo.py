import pytest

from src.modules.auth.domain.enums import StatusEnum, TypeEnum
from src.modules.auth.domain.user import User
from src.modules.auth.infra.user_repo import UserTortoiseRepo


@pytest.mark.asyncio
async def test_create_and_get_client():
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
    await UserTortoiseRepo.asave(entity=user_to_create)

    # when
    user_get_from_db = await UserTortoiseRepo.aget_first_from_filter(email=email)

    # then
    assert user_get_from_db.email == user_to_create.email
    assert user_get_from_db.email == email
    assert user_get_from_db.username == user_to_create.username
    assert user_get_from_db.first_name == user_to_create.first_name
    assert user_get_from_db.created_at is not None
    assert user_get_from_db.updated_at is not None


@pytest.mark.asyncio
async def test_create_multiple_and_get_all():
    # given
    num_of_users_to_create = 10
    users_to_create = [
        User.create(
            email=f"{i}@domain.com",
            password=f"{i}.test",
            username="test",
            first_name="test",
            last_name="test",
            status=StatusEnum.ACTIVE.value,
            type=TypeEnum.USER.value,
        )
        for i in range(num_of_users_to_create)
    ]
    for user in users_to_create:
        await UserTortoiseRepo.asave(entity=user)

    # when
    users_get_from_db = await UserTortoiseRepo.aget_all()

    # then
    assert num_of_users_to_create == len(users_get_from_db)
    allowed_emails = [u.email for u in users_to_create]
    allowed_usernames = [u.username for u in users_to_create]
    allowed_first_names = [u.first_name for u in users_to_create]

    for user in users_get_from_db:
        assert user.email in allowed_emails
        assert user.username in allowed_usernames
        assert user.first_name in allowed_first_names
        assert user.created_at is not None
        assert user.updated_at is not None


@pytest.mark.asyncio
async def test_update_user():
    # given
    email = "test@domain.com"
    user_to_update = User.create(
        email=email,
        password="test",
        username="test",
        first_name="test",
        last_name="test",
        status=StatusEnum.ACTIVE.value,
        type=TypeEnum.USER.value
    )
    await UserTortoiseRepo.asave(entity=user_to_update)

    # when
    new_username = "new_username"
    new_first_name = "new_first_name"
    user_to_update.username = new_username
    user_to_update.first_name = new_first_name
    await UserTortoiseRepo.aupdate(entity=user_to_update)

    # then
    user_get_from_db = await UserTortoiseRepo.aget_first_from_filter(email=email)
    assert user_get_from_db.username == new_username
    assert user_get_from_db.first_name == new_first_name
    assert user_get_from_db.updated_at > user_get_from_db.created_at
    assert user_get_from_db.email == user_get_from_db.email
