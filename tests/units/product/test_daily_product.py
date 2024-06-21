from unittest.mock import Mock

from uuid6 import uuid6

from src.core.domain.value_object import PrecisedFloat
from src.modules.product.domain.entity.consumption import DailyUserConsumption
from src.modules.product.domain.entity.daily_product import DailyUserProduct


def test_create_daily_product_based_on_product():
    # given
    user_id = uuid6()
    day = DailyUserConsumption.create(user_id=user_id)
    weight_in_grams = PrecisedFloat(120.20)

    product = Mock()
    product.id = uuid6()
    product.energy_kcal_100g = PrecisedFloat(55.6666)
    product.proteins_100g = PrecisedFloat(22.20)
    product.fat_100g = PrecisedFloat(55.20)
    product.carbohydrates_100g = PrecisedFloat(25.20)

    # when
    daily_product = DailyUserProduct.create(
        product=product, day=day, weight_in_grams=weight_in_grams
    )

    # then
    assert daily_product.id
    assert daily_product.created_at is not None
    assert daily_product.updated_at is not None
    assert daily_product.calories == 66.92
    assert daily_product.proteins == 26.68
    assert daily_product.fats == 66.35
    assert daily_product.carbohydrates == 30.29
    assert daily_product.weight_in_grams == weight_in_grams
