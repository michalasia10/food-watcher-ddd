from datetime import datetime, date, timedelta

import pytest
from uuid6 import uuid6

from src.modules.product_new.application.dto.daily_product import DailyUserProductInputDto
from src.modules.product_new.application.dto.product import ProductInputDto
from src.modules.product_new.domain.enum import UserProductType
from src.modules.product_new.domain.errors import ProductNotFound, DailyUserConsumptionNotFound
from src.modules.product_new.infra.repo.consumption import DailyUserConsumptionTortoiseRepo
from src.modules.product_new.infra.repo.daily_product import DailyUserProductTortoiseRepo


@pytest.mark.asyncio
async def test_add_meal_daily_consumption_not_exists(user_record, product_record, consumption_service):
    # given

    _date = datetime.now()
    dto = DailyUserProductInputDto(
        product_id=product_record.id,
        weight_in_grams=100,
        type=UserProductType.DINNER,
        date=_date
    )
    # sanity check [time should be 00:00:00]
    assert dto.date.day == _date.day
    assert dto.date.month == _date.month
    assert dto.date.year == _date.year

    if isinstance(dto.date, datetime):
        assert dto.date.hour == 0
        assert dto.date.minute == 0
        assert dto.date.second == 0
        assert dto.date.microsecond == 0
    elif isinstance(dto.date, date):
        assert not hasattr(dto.date, 'hour')
        assert not hasattr(dto.date, 'minute')
        assert not hasattr(dto.date, 'second')
        assert not hasattr(dto.date, 'microsecond')
    else:
        raise Exception("Invalid date type")

    # when

    daily_consumption = await consumption_service.add_meal(
        user_id=user_record.id,
        input_dto=dto
    )
    daily_consumption_from_db = await DailyUserConsumptionTortoiseRepo.aget_by_id(daily_consumption.id)
    daily_product_from_db = await DailyUserProductTortoiseRepo.aget_by_id(daily_consumption.products[0].id)

    # then
    assert daily_consumption_from_db is not None
    assert daily_product_from_db is not None

    assert daily_product_from_db.product_id == product_record.id
    assert daily_product_from_db.day_id == daily_consumption.id

    assert daily_consumption_from_db.user_id == user_record.id
    assert daily_consumption_from_db.date == dto.date


@pytest.mark.asyncio
async def test_add_meal_daily_consumption_exists(
        user_record,
        consumption_with_product,
        product_record,
        consumption_service
):
    # given
    dto = DailyUserProductInputDto(
        product_id=product_record.id,
        weight_in_grams=200,
        type=UserProductType.DINNER,
        date=consumption_with_product.date
    )

    # when
    daily_consumption = await consumption_service.add_meal(
        user_id=user_record.id,
        input_dto=dto
    )

    daily_consumption_from_db = await DailyUserConsumptionTortoiseRepo.aget_by_id(daily_consumption.id)
    daily_product_from_db_first = await DailyUserProductTortoiseRepo.aget_by_id(daily_consumption.products[0].id)
    daily_product_from_db_second = await DailyUserProductTortoiseRepo.aget_by_id(daily_consumption.products[1].id)

    # then
    assert len(daily_consumption.products) == 2
    assert daily_consumption.summary_calories == daily_consumption.summary_calories
    expected_summary_calories = daily_product_from_db_second.calories + daily_product_from_db_first.calories
    assert daily_consumption.summary_calories == expected_summary_calories

    assert daily_consumption_from_db is not None
    assert daily_product_from_db_first is not None
    assert daily_product_from_db_second is not None

    assert daily_product_from_db_first.product_id == product_record.id
    assert daily_product_from_db_first.day_id == daily_consumption.id

    assert daily_consumption_from_db.user_id == user_record.id
    assert daily_consumption_from_db.date == dto.date


@pytest.mark.asyncio
async def test_add_meal_product_not_found(user_record, consumption_service):
    # given
    dto = DailyUserProductInputDto(
        product_id=uuid6(),
        weight_in_grams=200,
        type=UserProductType.DINNER,
        date=datetime.now()
    )

    # when/then
    with pytest.raises(ProductNotFound):
        await consumption_service.add_meal(
            user_id=user_record.id,
            input_dto=dto
        )


@pytest.mark.asyncio
async def test_get_all_user_days(user_record, consumption_with_product, consumption_service):
    # given
    user_id = user_record.id

    # when
    days = await consumption_service.get_all_user_days(user_id=user_id)

    # then
    assert len(days) == 1
    assert days[0].id == consumption_with_product.id
    assert days[0].date.day == consumption_with_product.date.day
    assert days[0].date.month == consumption_with_product.date.month
    assert days[0].date.year == consumption_with_product.date.year


@pytest.mark.asyncio
async def test_get_all_user_days_dummy_user(consumption_service):
    # given
    user_id = uuid6()

    # when
    days = await consumption_service.get_all_user_days(user_id=user_id)

    # then
    assert len(days) == 0


@pytest.mark.asyncio
async def test_get_day_by_id(consumption_with_product, consumption_service):
    # given
    day_id = consumption_with_product.id

    # when
    day = await consumption_service.get_day_by_id(day_id=day_id)

    # then
    assert day is not None
    assert day.id == consumption_with_product.id
    assert day.date.day == consumption_with_product.date.day
    assert day.date.month == consumption_with_product.date.month
    assert day.date.year == consumption_with_product.date.year


@pytest.mark.asyncio
async def test_get_day_by_id_dummy_day(consumption_service):
    # given
    day_id = uuid6()

    # when/then
    with pytest.raises(DailyUserConsumptionNotFound):
        await consumption_service.get_day_by_id(day_id=day_id)


@pytest.mark.asyncio
async def test_get_day_by_datetime(consumption_with_product, consumption_service):
    # given/when
    day = await consumption_service.get_day_by_datetime(
        date=consumption_with_product.date,
        user_id=consumption_with_product.user_id
    )

    # then
    assert day is not None
    assert day.id == consumption_with_product.id
    assert day.date.day == consumption_with_product.date.day
    assert day.date.month == consumption_with_product.date.month
    assert day.date.year == consumption_with_product.date.year


@pytest.mark.asyncio
async def test_get_day_by_datetime_dummy_day(consumption_service, consumption_with_product):
    # given
    date = datetime.now() - timedelta(days=1)

    # when/then
    with pytest.raises(DailyUserConsumptionNotFound):
        await consumption_service.get_day_by_datetime(
            date=date,
            user_id=consumption_with_product.user_id
        )


@pytest.mark.asyncio
async def test_get_day_by_datetime_dummy_user(consumption_service, consumption_with_product):
    # when/then
    with pytest.raises(DailyUserConsumptionNotFound):
        await consumption_service.get_day_by_datetime(
            date=consumption_with_product.date,
            user_id=uuid6()
        )


@pytest.mark.asyncio
async def test_get_all_products(product_record, product_service):
    # when
    products = await product_service.get_all(skip=0, limit=10)

    # then
    assert len(products) == 1
    assert products[0].id == product_record.id
    assert products[0].name == product_record.name
    assert products[0].fat_100g == product_record.fat_100g
    assert products[0].carbohydrates_100g == product_record.carbohydrates_100g
    assert products[0].proteins_100g == product_record.proteins_100g
    assert products[0].energy_kcal_100g == product_record.energy_kcal_100g


@pytest.mark.asyncio
async def test_get_product_by_id(product_record, product_service):
    # when
    product = await product_service.get_by_id(id=product_record.id)

    # then
    assert product is not None
    assert product.id == product_record.id
    assert product.name == product_record.name
    assert product.fat_100g == product_record.fat_100g
    assert product.carbohydrates_100g == product_record.carbohydrates_100g
    assert product.proteins_100g == product_record.proteins_100g
    assert product.energy_kcal_100g == product_record.energy_kcal_100g


@pytest.mark.asyncio
async def test_get_product_by_id_dummy_product(product_service):
    # given
    product_id = uuid6()

    # when/then
    with pytest.raises(ProductNotFound):
        await product_service.get_by_id(id=product_id)


@pytest.mark.asyncio
async def test_create_product(product_service):
    # given
    dto = ProductInputDto(
        code=2,
        name='SOME_NAME',
        quantity='SOME_QUANTITY',
        brand='SOME_BRAND',
        size='SOME_SIZE',
        groups='SOME_GROUPS',
        category='SOME_CATEGORY',
        energy_kcal_100g=100.0,
        fat_100g=10.0,
        carbohydrates_100g=20.0,
        sugars_100g=30.0,
        proteins_100g=40.0
    )

    # when
    product = await product_service.create(input_dto=dto)

    # then
    assert product is not None
    assert product.name == dto.name
    assert product.fat_100g == dto.fat_100g
    assert product.carbohydrates_100g == dto.carbohydrates_100g


@pytest.mark.asyncio
async def test_update_product(product_record, product_service):
    # given
    dto = ProductInputDto(
        code=2,
        name='SOME_NAME',
        quantity='SOME_QUANTITY',
        brand='SOME_BRAND',
        size='SOME_SIZE',
        groups='SOME_GROUPS',
        category='SOME_CATEGORY',
        energy_kcal_100g=product_record.energy_kcal_100g + 10.0,
        fat_100g=product_record.fat_100g + 10.0,
        carbohydrates_100g=20.0,
        sugars_100g=30.0,
        proteins_100g=40.0
    )

    # when
    product = await product_service.update(id=product_record.id, input_dto=dto)

    # then
    assert product is not None
    assert product.id == product_record.id
    assert product.name == dto.name
    assert product.fat_100g == dto.fat_100g
    assert product.carbohydrates_100g == dto.carbohydrates_100g


@pytest.mark.asyncio
async def test_delete_product(product_record, product_service):
    # when
    await product_service.delete(id=product_record.id)

    # then
    with pytest.raises(ProductNotFound):
        await product_service.get_by_id(id=product_record.id)
