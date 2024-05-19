import pytest
from tortoise.exceptions import DoesNotExist

from src.core_new.infra.tortoiserepo import TortoiseRepo
from src.modules.auth_new.application.dto import UserInputDto, UserUpdateDto, UserAuthInputDto
from src.modules.auth_new.application.user_service import UserCrudService, AuthenticationService
from src.modules.auth_new.domain.errors import UserNotFound, BadCredentials
from src.modules.auth_new.domain.user import User


@pytest.mark.asyncio
async def test_user_service_create_user(user_service: UserCrudService, user_repo: TortoiseRepo):
    # given
    user_dto = UserInputDto(
        username="test",
        password="test",
        email="test@sth.com",
        first_name="test",
        last_name="test"
    )

    # when
    user = await user_service.create(user_dto)
    user_from_db = await user_repo.aget_by_id(user.id)

    # then
    for key, value in user_dto.dict().items():
        if key == "password":
            continue

        assert getattr(user_from_db, key) == value


@pytest.mark.asyncio
async def test_user_service_update_user(user_service: UserCrudService, user_repo: TortoiseRepo, user_record):
    # given
    u = await user_record
    user_dto = UserUpdateDto(email="sth@a.com")

    # when
    user = await user_service.update(u.id, user_dto)
    user_from_db = await user_repo.aget_by_id(user.id)

    # then
    assert user_from_db.email == user_dto.email


@pytest.mark.asyncio
async def test_user_service_delete_user(user_service: UserCrudService, user_repo: TortoiseRepo, user_record):
    # given
    u = await user_record

    # when
    await user_service.delete(u.id)

    # then
    with pytest.raises(DoesNotExist):
        await user_repo.aget_by_id(u.id)


@pytest.mark.asyncio
async def test_user_service_get_all(user_service: UserCrudService, user_record):
    # given
    u = await user_record

    # when
    users = await user_service.get_all(limit=10, skip=0)

    # then
    assert len(users) > 0
    assert u in users


@pytest.mark.asyncio
async def test_user_service_get_all(user_service: UserCrudService, user_record):
    # given
    u = await user_record

    # when
    user_db = await user_service.get_by_id(u.id)

    # then
    assert user_db == u


@pytest.mark.asyncio
async def test_auth_service_correct_pswd(auth_service: AuthenticationService, user_record, user_password):
    # given
    u = await user_record

    # when
    token = await auth_service.authenticate(
        credentials=UserAuthInputDto(
            username=u.username,
            password=user_password,
        )
    )

    # then
    assert token is not None
    assert token.user_id == u.id
    assert token.api_token is not None
    assert isinstance(token.api_token, str)


@pytest.mark.asyncio
async def test_auth_service_bad_username(auth_service: AuthenticationService, user_record, user_password):
    # given
    await user_record

    # when/then
    with pytest.raises(UserNotFound):
        await auth_service.authenticate(
            credentials=UserAuthInputDto(
                username="bad_username",
                password=user_password,
            )
        )


@pytest.mark.asyncio
async def test_auth_service_bad_pswd(auth_service: AuthenticationService, user_record):
    # given
    u = await user_record

    # when/then
    with pytest.raises(BadCredentials):
        await auth_service.authenticate(
            credentials=UserAuthInputDto(
                username=u.username,
                password='bad_password',
            )
        )


@pytest.mark.asyncio
async def test_auth_service_user_not_found_bad_token(
        auth_service: AuthenticationService, user_record, secret_key: str, algorithm: str
):
    # given
    u = await user_record
    dummy_user_not_in_db = User.create(
        username="dummy",
        password="dummy",
        email="dummy@wp.pl",
        first_name="dummy",
        last_name="dummy"
    )
    dumy_token = dummy_user_not_in_db.create_token(
        secret_key=secret_key,
        algorithm=algorithm
    )

    # sanity check
    assert dumy_token is not None
    assert u.id != dummy_user_not_in_db.id

    # when/then
    with pytest.raises(BadCredentials):
        await auth_service.verify(token=dumy_token)


@pytest.mark.asyncio
async def test_auth_service_correct_token(auth_service: AuthenticationService, user_record, user_password):
    # given
    user = await user_record
    token = await auth_service.authenticate(
        credentials=UserAuthInputDto(
            username=user.username,
            password=user_password
        )
    )
    # sanity check
    assert token is not None
    assert token.user_id == user.id
    assert token.api_token is not None

    # when
    user_from_token = await auth_service.verify(token=token.api_token)

    # then
    assert user_from_token.id == user.id
