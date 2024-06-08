from datetime import datetime
from unittest.mock import Mock

from uuid6 import uuid6

from src.modules.recipe_new.domain.entity.recipe import Recipe
from src.core_new.domain.value_object import PrecisedFloat
from src.modules.recipe_new.domain.entity.recipe_product import ProductForRecipe


def test_create_product_for_recipe():
    product = Mock()
    product.energy_kcal_100g = PrecisedFloat(100)
    product.proteins_100g = PrecisedFloat(10)
    product.fat_100g = PrecisedFloat(10)
    product.carbohydrates_100g = PrecisedFloat(10)

    recipe = Recipe.create(
        name="test",
        link="url.com",
        description="sth",
        user_id=uuid6()
    )
    product_for_recipe = ProductForRecipe.create(
        recipe=recipe,
        product=product,
        weight_in_grams=PrecisedFloat(222.2)
    )

    assert product_for_recipe.calories == 222.2
    assert product_for_recipe.proteins == 22.22
    assert product_for_recipe.fats == 22.22
    assert product_for_recipe.carbohydrates == 22.22

    assert recipe.summary_fats == 22.22
    assert recipe.summary_proteins == 22.22
    assert recipe.summary_carbohydrates == 22.22
    assert recipe.summary_calories == 222.2


def test_update_product_for_recipe():
    # given
    product = Mock()
    product.energy_kcal_100g = PrecisedFloat(100)
    product.proteins_100g = PrecisedFloat(5.75)
    product.fat_100g = PrecisedFloat(22.5)
    product.carbohydrates_100g = PrecisedFloat(55.1)

    recipe = Mock()
    recipe.add_product = Mock()
    recipe.delete_product = Mock()

    product_for_recipe = ProductForRecipe(
        id=uuid6(),
        product=product,
        weight_in_grams=PrecisedFloat(100.0),
        calories=product.energy_kcal_100g,
        proteins=product.proteins_100g,
        fats=product.fat_100g,
        carbohydrates=product.carbohydrates_100g,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    # when
    product_for_recipe.update_weight(recipe=recipe, weight=44.5)

    # then
    assert product_for_recipe.calories == 44.5
    assert product_for_recipe.proteins == 2.56
    assert product_for_recipe.carbohydrates == 24.52
    assert product_for_recipe.fats == 10.01
