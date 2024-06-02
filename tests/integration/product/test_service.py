from datetime import datetime, date

import pytest

from src.modules.product_new.domain.enum import UserProductType
from src.modules.product_new.application.dto.daily_product import DailyUserProductInputDto
from src.modules.product_new.infra.repo.daily_product import DailyUserProductTortoiseRepo
from src.modules.product_new.infra.repo.consumption import DailyUserConsumptionTortoiseRepo


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
