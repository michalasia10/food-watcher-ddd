from unittest.mock import Mock

from uuid6 import uuid6

from src.core_new.domain.value_object import PrecisedFloat
from src.modules.product_new.domain.entity.consumption import DailyUserConsumption


def test_create_daily_user_consumption_entity():
    # given
    user_id = uuid6()

    # when
    daily_user_consumption = DailyUserConsumption.create(user_id)

    # then
    assert daily_user_consumption.id
    assert daily_user_consumption.created_at is not None
    assert daily_user_consumption.updated_at is not None
    assert daily_user_consumption.user_id == user_id
    assert daily_user_consumption.date is not None
    assert daily_user_consumption.products == []
    assert daily_user_consumption.summary_proteins == 0.0
    assert daily_user_consumption.summary_fats == 0.0
    assert daily_user_consumption.summary_carbohydrates == 0.0
    assert daily_user_consumption.summary_calories == 0.0


def test_add_product_to_daily_user_consumption_entity():
    # given
    user_id = uuid6()
    daily_user_consumption = DailyUserConsumption.create(user_id)

    product = Mock()
    product.calories = PrecisedFloat(100)
    product.weight_in_grams = PrecisedFloat(100)
    product.proteins = PrecisedFloat(10)
    product.fats = PrecisedFloat(10)
    product.carbohydrates = PrecisedFloat(10)

    # when
    daily_user_consumption.add_product(product)

    # then
    assert daily_user_consumption.summary_fats == 10
    assert daily_user_consumption.summary_proteins == 10
    assert daily_user_consumption.summary_carbohydrates == 10
    assert daily_user_consumption.summary_calories == 100


def test_add_multiple_products_to_daily_user_consumption_entity():
    # given
    user_id = uuid6()
    daily_user_consumption = DailyUserConsumption.create(user_id)

    product_1 = Mock()
    product_1.calories = PrecisedFloat(100.20)
    product_1.weight_in_grams = PrecisedFloat(100.20)
    product_1.proteins = PrecisedFloat(10.20)
    product_1.fats = PrecisedFloat(10.20)
    product_1.carbohydrates = PrecisedFloat(10.20)

    product_2 = Mock()
    product_2.calories = PrecisedFloat(200.40)
    product_2.weight_in_grams = PrecisedFloat(200.40)
    product_2.proteins = PrecisedFloat(20.40)
    product_2.fats = PrecisedFloat(20.40)
    product_2.carbohydrates = PrecisedFloat(20.40)

    # when
    daily_user_consumption.add_product(product_1)
    daily_user_consumption.add_product(product_2)

    # then
    assert daily_user_consumption.summary_fats == 30.60
    assert daily_user_consumption.summary_proteins == 30.60
    assert daily_user_consumption.summary_carbohydrates == 30.60
    assert daily_user_consumption.summary_calories == 300.60


def test_delete_product_from_daily_user_consumption_entity():
    # given
    user_id = uuid6()
    daily_user_consumption = DailyUserConsumption.create(user_id)

    product_1 = Mock()
    product_1.calories = PrecisedFloat(100.20)
    product_1.weight_in_grams = PrecisedFloat(100.20)
    product_1.proteins = PrecisedFloat(10.20)
    product_1.fats = PrecisedFloat(10.20)
    product_1.carbohydrates = PrecisedFloat(10.20)

    product_2 = Mock()
    product_2.calories = PrecisedFloat(200.40)
    product_2.weight_in_grams = PrecisedFloat(200.40)
    product_2.proteins = PrecisedFloat(20.40)
    product_2.fats = PrecisedFloat(20.40)
    product_2.carbohydrates = PrecisedFloat(20.40)

    daily_user_consumption.add_product(product_1)
    daily_user_consumption.add_product(product_2)

    # sanity check

    assert daily_user_consumption.summary_calories == 300.60

    # when

    daily_user_consumption.delete_product(product_2)

    # then

    assert daily_user_consumption.summary_fats == 10.20
    assert daily_user_consumption.summary_proteins == 10.20
    assert daily_user_consumption.summary_carbohydrates == 10.20
    assert daily_user_consumption.summary_calories == 100.20
