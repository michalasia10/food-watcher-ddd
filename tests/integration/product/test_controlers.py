from datetime import datetime, timedelta
from http import HTTPStatus

import pytest
from uuid6 import uuid6

from src.modules.product.application.dto.daily_product import DailyUserProductInputDto
from src.modules.product.application.dto.product import ProductInputDto
from src.modules.product.domain.enum import UserProductType
from src.modules.product.infra.repo.consumption import DailyUserConsumptionTortoiseRepo
from src.modules.product.infra.repo.daily_product import DailyUserProductTortoiseRepo
from src.modules.product.infra.repo.product import ProductTortoiseRepo


@pytest.mark.asyncio
async def test_product_controller_create_product(api_client, endpoint_enum, user_token):
    # given
    api_client.set_token(user_token.api_token)

    product_input = ProductInputDto(
        code=222,
        name="test_api",
        quantity="test_api",
        brand="test_api",
        size="test_api",
        groups="test_api",
        category="test_api",
        energy_kcal_100g=22.2,
        fat_100g=22.2,
        carbohydrates_100g=22.2,
        sugars_100g=22.2,
        proteins_100g=22.3,
    )
    # when
    response = await api_client.post(
        endpoint_enum.PRODUCTS.value, json_data=product_input.dict()
    )

    # then
    assert response.status_code == HTTPStatus.CREATED
    product_from_db = await ProductTortoiseRepo.aget_first_from_filter(
        code=product_input.code
    )
    response_json = response.json()

    api_client.compare_response_object_with_db(
        response_json, product_from_db, product_input
    )


@pytest.mark.asyncio
async def test_product_controller_get_all_products(
    api_client, endpoint_enum, product_record, user_token
):
    # given
    api_client.set_token(user_token.api_token)

    # when
    response = await api_client.get(endpoint_enum.PRODUCTS.value)

    # then
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert len(response_json) == 1

    api_client.compare_response_object_with_db(response_json[0], product_record)


@pytest.mark.asyncio
async def test_product_controller_get_product_by_id(
    api_client, endpoint_enum, product_record, user_token
):
    # given
    api_client.set_token(user_token.api_token)

    # when
    response = await api_client.get(
        endpoint_enum.PRODUCTS.get_detail(product_record.id)
    )

    # then
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()

    api_client.compare_response_object_with_db(response_json, product_record)


@pytest.mark.asyncio
async def test_consumption_controller_create_consumption(
    api_client, endpoint_enum, user_record, product_record, user_token
):
    # given
    daily_product_input = DailyUserProductInputDto(
        product_id=product_record.id,
        weight_in_grams=100.5,
        type=UserProductType.BREAKFAST,
        date=datetime.now(),
    )
    api_client.set_token(user_token.api_token)

    # when
    response = await api_client.post(
        endpoint_enum.CONSUMPTION, json_data=daily_product_input.model_dump_json()
    )

    # then

    daily_consumption_from_db = (
        await DailyUserConsumptionTortoiseRepo.aget_first_from_filter(
            date=daily_product_input.date
        )
    )
    daily_product_from_db = await DailyUserProductTortoiseRepo.aget_first_from_filter(
        product_id=product_record.id, day_id=daily_consumption_from_db.id
    )

    # then
    assert response.status_code == HTTPStatus.CREATED
    assert daily_consumption_from_db is not None
    assert daily_product_from_db is not None


@pytest.mark.asyncio
async def test_consumption_controller_add_meal_consumption_exists(
    api_client,
    endpoint_enum,
    user_record,
    product_record,
    user_token,
    consumption_with_product,
):
    # given
    daily_product_input = DailyUserProductInputDto(
        product_id=product_record.id,
        weight_in_grams=100.5,
        type=UserProductType.BREAKFAST,
        date=consumption_with_product.date,
    )
    api_client.set_token(user_token.api_token)

    # when
    response = await api_client.post(
        endpoint_enum.CONSUMPTION, json_data=daily_product_input.model_dump_json()
    )

    # then
    assert response.status_code == HTTPStatus.CREATED
    daily_consumption_from_db = (
        await DailyUserConsumptionTortoiseRepo.aget_first_from_filter(
            date=daily_product_input.date
        )
    )
    daily_products_from_db = await DailyUserProductTortoiseRepo.aget_all_from_filter(
        day_id=daily_consumption_from_db.id
    )

    # then
    assert response.status_code == HTTPStatus.CREATED
    assert daily_consumption_from_db is not None
    assert len(daily_products_from_db) == 2


@pytest.mark.asyncio
async def test_consumption_controller_add_meal_product_not_found(
    api_client,
    endpoint_enum,
    user_record,
    user_token,
    consumption_with_product,
):
    # given
    daily_product_input = DailyUserProductInputDto(
        product_id=uuid6(),
        weight_in_grams=100.5,
        type=UserProductType.BREAKFAST,
        date=consumption_with_product.date,
    )
    api_client.set_token(user_token.api_token)

    # when
    response = await api_client.post(
        endpoint_enum.CONSUMPTION, json_data=daily_product_input.model_dump_json()
    )

    # then
    api_client.check_status_code_in_error_response(response, HTTPStatus.NOT_FOUND)


@pytest.mark.asyncio
async def test_consumption_controller_get_all_user_days(
    api_client, endpoint_enum, user_record, user_token, consumption_with_product
):
    # given
    api_client.set_token(user_token.api_token)

    # when
    response = await api_client.get(endpoint_enum.CONSUMPTION.get_detail("by_user_id/"))

    # then
    assert response.status_code == HTTPStatus.OK
    days = response.json()

    assert len(days) == 1
    day = days[0]
    assert "user_id" in day
    assert "date" in day
    assert "products" in day
    assert "summary_calories" in day
    assert "summary_proteins" in day
    assert "summary_fats" in day
    assert "summary_carbohydrates" in day

    products = day["products"]
    assert len(products) == 1
    product = products[0]

    assert "product_id" in product
    assert "product" in product

    product = product["product"]
    assert "id" in product
    assert "name" in product


@pytest.mark.asyncio
async def test_consumption_controller_get_all_user_days_dummy_user(
    api_client, endpoint_enum, user_token
):
    # given
    api_client.set_token(user_token.api_token)

    # when
    response = await api_client.get(endpoint_enum.CONSUMPTION.get_detail("by_user_id/"))

    # then
    assert response.status_code == HTTPStatus.OK
    days = response.json()
    assert len(days) == 0


@pytest.mark.asyncio
async def test_consumption_controller_get_day_by_id(
    api_client, endpoint_enum, user_token, consumption_with_product
):
    # given
    api_client.set_token(user_token.api_token)

    # when
    response = await api_client.get(
        endpoint_enum.CONSUMPTION.get_detail(f"by_day_id/{consumption_with_product.id}")
    )

    # then
    assert response.status_code == HTTPStatus.OK
    day = response.json()

    assert day
    assert str(day["id"]) == str(consumption_with_product.id)


@pytest.mark.asyncio
async def test_consumption_controller_get_day_by_id_dummy_day(
    api_client, endpoint_enum, user_token
):
    # given
    day_id = uuid6()
    api_client.set_token(user_token.api_token)

    # when
    response = await api_client.get(
        endpoint_enum.CONSUMPTION.get_detail(f"by_day_id/{str(uuid6())}")
    )

    # then
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_consumption_controller_get_day_by_datetime(
    api_client, endpoint_enum, user_token, consumption_with_product
):
    # given
    api_client.set_token(user_token.api_token)
    date_str = str(consumption_with_product.date)

    # when
    response = await api_client.get(
        endpoint_enum.CONSUMPTION.get_detail(f"by_datetime_for_user/{date_str}/")
    )

    # then
    assert response.status_code == HTTPStatus.OK
    day = response.json()

    assert day["id"] == str(consumption_with_product.id)


@pytest.mark.asyncio
async def test_consumption_controller_get_day_by_datetime_dummy_day(
    api_client, endpoint_enum, user_token, consumption_with_product
):
    # given
    api_client.set_token(user_token.api_token)
    date_str = str(datetime.now() - timedelta(days=1))

    # when
    response = await api_client.get(
        endpoint_enum.CONSUMPTION.get_detail(f"by_datetime_for_user/{date_str}/")
    )

    # then
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_consumption_controller_get_day_by_datetime_dummy_user(
    api_client, endpoint_enum, user_token, user_token2, consumption_with_product
):
    # given
    api_client.set_token(user_token2.api_token)
    date_str = str(consumption_with_product.date)

    # when
    response = await api_client.get(
        endpoint_enum.CONSUMPTION.get_detail(f"by_datetime_for_user/{date_str}/")
    )

    # then
    assert response.status_code == HTTPStatus.NOT_FOUND
