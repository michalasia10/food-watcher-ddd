import uuid
from http import HTTPStatus

import pytest

from src.modules.auth.application.dto import (
    UserInputDto,
    UserUpdateDto,
    UserAuthInputDto,
    UserSettingsDto,
)
from src.modules.auth.infra.repo.user import UserTortoiseRepo


@pytest.mark.asyncio
async def test_user_controller_create_user(api_client, endpoint_enum):
    # given
    user_input = UserInputDto(
        username="test_api",
        password="test_api",
        email="test_api@user.com",
        first_name="test_api",
        last_name="test_api",
        settings=UserSettingsDto(
            age=20,
        ),
    )
    # when
    response = await api_client.post(endpoint_enum.USERS.value, json_data=user_input.model_dump_json())

    # then
    assert response.status_code == HTTPStatus.CREATED
    response_json = response.json()
    assert response_json["username"] == user_input.username
    assert response_json["email"] == user_input.email
    users = await UserTortoiseRepo.aget_all()
    assert len(users) > 0
    user_from_db = await UserTortoiseRepo.aget_by_id(response_json["id"])
    assert user_from_db.username == user_input.username


@pytest.mark.asyncio
async def test_user_controller_get_all_users(api_client, endpoint_enum, user_record):
    # when
    response = await api_client.get(endpoint_enum.USERS.value)

    # then
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert len(response_json) == 1
    assert response_json[0]["username"] == user_record.username
    assert response_json[0]["email"] == user_record.email
    assert response_json[0]["first_name"] == user_record.first_name


@pytest.mark.asyncio
async def test_user_controller_get_user_by_id(api_client, endpoint_enum, user_record):
    # given/when
    response = await api_client.get(endpoint_enum.USERS.get_detail(user_record.id))

    # then
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert response_json["username"] == user_record.username
    assert response_json["email"] == user_record.email
    assert response_json["first_name"] == user_record.first_name


@pytest.mark.asyncio
async def test_user_controller_get_user_by_id_not_found(api_client, endpoint_enum):
    # given
    not_existing_id = str(uuid.uuid4())

    # when
    response = await api_client.get(endpoint_enum.USERS.get_detail(not_existing_id))

    # then
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_user_controller_update_user(api_client, endpoint_enum, user_record, user_token):
    # given
    new_email = "new_test@email.com"
    update_dto = UserUpdateDto(email=new_email)
    api_client.set_token(user_token.api_token)

    # when
    response = await api_client.put(
        endpoint_enum.USERS.get_detail(user_token.user_id),
        json_data=update_dto.model_dump_json(),
    )

    # then
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert response_json["email"] == new_email
    user_from_db = await UserTortoiseRepo.aget_by_id(user_token.user_id)
    assert user_from_db.email == new_email


@pytest.mark.asyncio
async def test_user_controller_update_user_dummy_token(api_client, endpoint_enum, user_record, dummy_token):
    # given
    new_email = "new@email.com"
    update_dto = UserUpdateDto(email=new_email)
    api_client.set_token(dummy_token.api_token)

    # when
    response = await api_client.put(
        endpoint_enum.USERS.get_detail(user_record.id),
        json_data=update_dto.model_dump_json(),
    )

    # then
    api_client.check_status_code_in_error_response(response, HTTPStatus.UNAUTHORIZED)
    user_from_db = await UserTortoiseRepo.aget_by_id(user_record.id)
    assert user_from_db.email != new_email


@pytest.mark.asyncio
async def test_user_controller_update_requestor_not_owner_of_record(
    api_client, endpoint_enum, user_record, user_token2
):
    # given
    new_email = "new@email.com"
    update_dto = UserUpdateDto(email=new_email)
    api_client.set_token(user_token2.api_token)

    # when
    response = await api_client.put(
        endpoint_enum.USERS.get_detail(user_record.id),
        json_data=update_dto.model_dump_json(),
    )

    # then
    api_client.check_status_code_in_error_response(response, HTTPStatus.FORBIDDEN)
    user_from_db = await UserTortoiseRepo.aget_by_id(user_record.id)
    assert user_from_db.email != new_email


@pytest.mark.asyncio
async def test_user_controller_delete_user(api_client, endpoint_enum, user_record, user_token):
    # given
    api_client.set_token(user_token.api_token)

    # when
    response = await api_client.delete(endpoint_enum.USERS.get_detail(user_token.user_id))

    # then
    assert response.status_code == HTTPStatus.NO_CONTENT
    users = await UserTortoiseRepo.aget_all()
    assert len(users) == 0


@pytest.mark.asyncio
async def test_user_controller_delete_user_dummy_token(api_client, endpoint_enum, user_record, dummy_token):
    # given
    api_client.set_token(dummy_token.api_token)

    # when
    response = await api_client.delete(endpoint_enum.USERS.get_detail(user_record.id))

    # then
    api_client.check_status_code_in_error_response(response, HTTPStatus.UNAUTHORIZED)
    users = await UserTortoiseRepo.aget_all()
    assert len(users) == 1


@pytest.mark.asyncio
async def test_user_controller_delete_requestor_not_owner_of_record(
    api_client, endpoint_enum, user_record, user_token2
):
    # given
    api_client.set_token(user_token2.api_token)

    # when
    response = await api_client.delete(endpoint_enum.USERS.get_detail(user_record.id))

    # then
    api_client.check_status_code_in_error_response(response, HTTPStatus.FORBIDDEN)
    users = await UserTortoiseRepo.aget_all()
    assert len(users) == 2


@pytest.mark.asyncio
async def test_user_get_all_users(api_client, endpoint_enum, user_record, user_record2):
    # when
    response = await api_client.get(endpoint_enum.USERS.value)

    # then
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert len(response_json) == 2

    def test_user_response(u_record, response_json):
        assert response_json["username"] == u_record.username
        assert response_json["email"] == u_record.email
        assert response_json["first_name"] == u_record.first_name
        assert response_json["last_name"] == u_record.last_name

    test_user_response(user_record, response_json[0])
    test_user_response(user_record2, response_json[1])


@pytest.mark.asyncio
async def test_user_login(api_client, endpoint_enum, user_record, user_password):
    # given
    login_dto = UserAuthInputDto(username=user_record.username, password=user_password)

    # when
    response = await api_client.post(
        f"{endpoint_enum.USERS.value}login/",
        json_data=login_dto.model_dump_json(),
    )

    # then
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert "api_token" in response_json
    assert "user_id" in response_json
    assert response_json["user_id"] == str(user_record.id)
    assert isinstance(response_json["api_token"], str)


@pytest.mark.asyncio
async def test_user_login_wrong_password(api_client, endpoint_enum, user_record):
    # given
    login_dto = UserAuthInputDto(username=user_record.username, password="wrong_password")

    # when
    response = await api_client.post(
        f"{endpoint_enum.USERS.value}login/",
        json_data=login_dto.model_dump_json(),
    )

    # then
    api_client.check_status_code_in_error_response(response, HTTPStatus.UNAUTHORIZED)


@pytest.mark.asyncio
async def test_user_login_wrong_username(api_client, endpoint_enum, user_record, user_password):
    # given
    login_dto = UserAuthInputDto(username="wrong_username", password=user_password)

    # when
    response = await api_client.post(
        f"{endpoint_enum.USERS.value}login/",
        json_data=login_dto.model_dump_json(),
    )

    # then
    api_client.check_status_code_in_error_response(response, HTTPStatus.UNAUTHORIZED)


@pytest.mark.asyncio
async def test_user_controller_refresh_token(api_client, endpoint_enum, user_record, user_token):
    # given
    api_client.set_token(user_token.api_token)

    # when
    response = await api_client.post(endpoint_enum.USERS.get_detail("refresh_token"))

    # then
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert "api_token" in response_json
    assert "user_id" in response_json
    assert response_json["user_id"] == str(user_record.id)
    assert isinstance(response_json["api_token"], str)

    assert user_token.api_token != response_json["api_token"]
