from http import HTTPStatus

import pytest

from src.modules.auth_new.application.dto import UserInputDto, UserUpdateDto
from src.modules.auth_new.infra.user_repo import UserTortoiseRepo


@pytest.mark.asyncio
async def test_user_controller_create_user(api_client, endpoint_enum):
    # given
    user_input = UserInputDto(
        username="test_api",
        password="test_api",
        email="test_api@user.com",
        first_name="test_api",
        last_name="test_api"
    )
    # when
    response = await api_client.post(endpoint_enum.USERS.value, json=user_input.dict())

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
async def test_user_controller_update_user(api_client, endpoint_enum, user_record, user_token):
    # given
    new_email = "new_test@email.com"
    update_dto = UserUpdateDto(email=new_email)
    api_client.set_token(user_token.api_token)

    # when
    response = await api_client.put(
        endpoint_enum.USERS.get_detail(user_token.user_id),
        json=update_dto.dict(),
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
        json=update_dto.dict(),
    )

    # then
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    user_from_db = await UserTortoiseRepo.aget_by_id(user_record.id)
    assert user_from_db.email != new_email
    api_client.check_correct_keys_in_error_response(response.json())


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
        json=update_dto.dict(),
    )

    # then
    assert response.status_code == HTTPStatus.FORBIDDEN
    user_from_db = await UserTortoiseRepo.aget_by_id(user_record.id)
    assert user_from_db.email != new_email
    api_client.check_correct_keys_in_error_response(response.json())
