from unittest.mock import Mock

from uuid6 import uuid6

from src.core.domain.value_object import PrecisedFloat
from src.modules.recipe.domain.entity.recipe import Recipe


def test_create_recipe():
    recipe = Recipe.create(
        name="test", link="url.com", description="sth", user_id=uuid6()
    )
    assert recipe.created_at is not None
    assert recipe.updated_at is not None
    assert recipe.summary_calories == PrecisedFloat(0.0)
    assert recipe.summary_fats == PrecisedFloat(0.0)
    assert recipe.summary_proteins == PrecisedFloat(0.0)
    assert recipe.summary_proteins == PrecisedFloat(0.0)


def test_add_product_to_recipe():
    # given
    product = Mock()
    product.calories = PrecisedFloat(100)
    product.weight_in_grams = PrecisedFloat(100)
    product.proteins = PrecisedFloat(10)
    product.fats = PrecisedFloat(10)
    product.carbohydrates = PrecisedFloat(10)

    recipe = Recipe.create(
        name="test", link="url.com", description="sth", user_id=uuid6()
    )

    # when
    recipe.add_product(product)

    # then
    assert recipe.summary_fats == 10
    assert recipe.summary_proteins == 10
    assert recipe.summary_carbohydrates == 10
    assert recipe.summary_calories == 100


def test_delete_from_recipe():
    # given

    product = Mock()
    product.calories = PrecisedFloat(100)
    product.weight_in_grams = PrecisedFloat(100)
    product.proteins = PrecisedFloat(10)
    product.fats = PrecisedFloat(10)
    product.carbohydrates = PrecisedFloat(10)

    product2 = Mock()
    product2.calories = PrecisedFloat(120)
    product2.weight_in_grams = PrecisedFloat(150)
    product2.proteins = PrecisedFloat(20)
    product2.fats = PrecisedFloat(30)
    product2.carbohydrates = PrecisedFloat(40)

    recipe = Recipe.create(
        name="test", link="url.com", description="sth", user_id=uuid6()
    )

    recipe.add_product(product)
    recipe.add_product(product2)

    # when

    recipe.delete_product(product)

    # then
    assert recipe.summary_proteins == 20
    assert recipe.summary_fats == 30
    assert recipe.summary_carbohydrates == 40
    assert recipe.summary_calories == 120
