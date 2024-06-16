from copy import deepcopy

import pytest
from uuid6 import uuid6

from src.modules.recipe_new.application.dto.recipe import RecipeInputDto, RecipeUpdateDto
from src.modules.recipe_new.application.dto.recipe_product import ProductForRecipeInputDto, ProductForRecipeUpdateDto
from src.modules.recipe_new.domain.errors import RecipeNotFound, RecipeNotRecordOwner, ProductForRecipeNotRecordOwner, \
    ProductForRecipeNotFound


@pytest.mark.asyncio
async def test_recipe_service_get_all(recipe_record, recipe_service):
    # when
    recipes = await recipe_service.get_all()

    # then
    assert len(recipes) == 1


@pytest.mark.asyncio
async def test_recipe_service_get_all_my_recipes(recipe_record, recipe_service):
    # when
    recipes = await recipe_service.get_all_my_recipes(user_id=recipe_record.user_id)

    # then
    assert len(recipes) == 1
    assert recipes[0].user_id == recipe_record.user_id


@pytest.mark.asyncio
async def test_recipe_service_get_all_my_recipes_dummy_user(recipe_record, recipe_service):
    # when
    recipes = await recipe_service.get_all_my_recipes(user_id=uuid6())

    # then
    assert len(recipes) == 0


@pytest.mark.asyncio
async def test_recipe_service_get_by_id(recipe_record, recipe_service):
    # when
    recipe = await recipe_service.get_by_id(recipe_record.id)

    # then
    assert recipe.id == recipe_record.id
    assert recipe.user_id == recipe_record.user_id


@pytest.mark.asyncio
async def test_recipe_service_get_by_id_not_found(recipe_record, recipe_service):
    # when/then
    with pytest.raises(RecipeNotFound):
        await recipe_service.get_by_id(uuid6())


@pytest.mark.asyncio
async def test_recipe_service_create(recipe_service, user_record, product_record):
    # given
    weight_in_grams = 20.56
    recipe_input = RecipeInputDto(
        name='recipe',
        products=[
            ProductForRecipeInputDto(
                product_id=product_record.id,
                weight_in_grams=weight_in_grams,
            )
        ]
    )

    # when
    recipe = await recipe_service.create(user_id=user_record.id, input_dto=recipe_input)

    # then
    assert recipe.name == 'recipe'
    assert len(recipe.products_for_recipe) == 1
    product_for_recipe = recipe.products_for_recipe[0]

    assert product_for_recipe.product_id == product_record.id
    assert product_for_recipe.weight_in_grams == weight_in_grams
    assert product_for_recipe.carbohydrates == 4.11
    assert product_for_recipe.proteins == 8.22
    assert product_for_recipe.fats == 2.06
    assert product_for_recipe.calories == 20.56

    assert recipe.summary_proteins == 8.22
    assert recipe.summary_fats == 2.06
    assert recipe.summary_carbohydrates == 4.11
    assert recipe.summary_calories == 20.56


@pytest.mark.asyncio
async def test_recipe_service_create_multiple_products(recipe_service, user_record, product_record, product_record2):
    # given
    weight_in_grams = 20.56
    weight_in_grams2 = 30.56
    recipe_input = RecipeInputDto(
        name='recipe',
        products=[
            ProductForRecipeInputDto(
                product_id=product_record.id,
                weight_in_grams=weight_in_grams,
            ),
            ProductForRecipeInputDto(
                product_id=product_record2.id,
                weight_in_grams=weight_in_grams2,
            )
        ]
    )

    # when
    recipe = await recipe_service.create(user_id=user_record.id, input_dto=recipe_input)

    # then
    assert recipe.name == 'recipe'
    assert len(recipe.products_for_recipe) == 2
    product_for_recipe = recipe.products_for_recipe[0]
    product_for_recipe2 = recipe.products_for_recipe[1]

    assert product_for_recipe.product_id == product_record.id
    assert product_for_recipe.weight_in_grams == weight_in_grams
    assert product_for_recipe.carbohydrates == 4.11
    assert product_for_recipe.proteins == 8.22
    assert product_for_recipe.fats == 2.06
    assert product_for_recipe.calories == 20.56

    assert product_for_recipe2.product_id == product_record2.id
    assert product_for_recipe2.weight_in_grams == weight_in_grams2
    assert product_for_recipe2.carbohydrates == 10.22
    assert product_for_recipe2.proteins == 12.22
    assert product_for_recipe2.fats == 6.79
    assert product_for_recipe2.calories == 16.98

    assert recipe.summary_proteins == 20.44
    assert recipe.summary_fats == 8.85
    assert recipe.summary_carbohydrates == 14.33
    assert recipe.summary_calories == 37.54


@pytest.mark.asyncio
async def test_recipe_service_update(recipe_record, recipe_service):
    # given
    new_name = 'new name'
    update_dto = RecipeUpdateDto(
        name=new_name
    )

    # when
    recipe = await recipe_service.update(
        id=recipe_record.id,
        input_dto=update_dto,
        user_id=recipe_record.user_id
    )

    # then
    assert recipe.name == 'new name'
    assert recipe.user_id == recipe_record.user_id
    assert recipe.summary_proteins == recipe_record.summary_proteins
    assert recipe.summary_fats == recipe_record.summary_fats
    assert recipe.summary_carbohydrates == recipe_record.summary_carbohydrates


@pytest.mark.asyncio
async def test_recipe_service_update_not_found(recipe_record, recipe_service):
    # given
    new_name = 'new name'
    update_dto = RecipeUpdateDto(
        name=new_name
    )

    # when/then
    with pytest.raises(RecipeNotFound):
        await recipe_service.update(
            id=uuid6(),
            input_dto=update_dto,
            user_id=recipe_record.user_id
        )


@pytest.mark.asyncio
async def test_recipe_service_update_wrong_user(recipe_record, recipe_service):
    # given
    new_name = 'new name'
    update_dto = RecipeUpdateDto(
        name=new_name
    )

    # when/then
    with pytest.raises(RecipeNotRecordOwner):
        await recipe_service.update(
            id=recipe_record.id,
            input_dto=update_dto,
            user_id=uuid6()
        )


@pytest.mark.asyncio
async def test_recipe_service_delete(recipe_record, recipe_service):
    # when
    await recipe_service.delete(id=recipe_record.id, user_id=recipe_record.user_id)

    # then
    with pytest.raises(RecipeNotFound):
        await recipe_service.get_by_id(recipe_record.id)


@pytest.mark.asyncio
async def test_recipe_service_delete_not_found(recipe_record, recipe_service):
    # when/then
    with pytest.raises(RecipeNotFound):
        await recipe_service.delete(id=uuid6(), user_id=recipe_record.user_id)


@pytest.mark.asyncio
async def test_recipe_service_delete_wrong_user(recipe_record, recipe_service):
    # when/then
    with pytest.raises(RecipeNotRecordOwner):
        await recipe_service.delete(
            id=recipe_record.id,
            user_id=uuid6(),
        )


@pytest.mark.asyncio
async def test_recipe_service_add_product_to_recipe(recipe_record_with_products, product_record, product_record2,
                                                    recipe_service):
    # given
    weight_in_grams = 120.56
    product_for_recipe_input = ProductForRecipeInputDto(
        product_id=product_record.id,
        weight_in_grams=weight_in_grams
    )
    old_recipe_sum_proteins = deepcopy(recipe_record_with_products.summary_proteins)
    old_recipe_sum_fats = deepcopy(recipe_record_with_products.summary_fats)
    old_recipe_sum_carbohydrates = deepcopy(recipe_record_with_products.summary_carbohydrates)
    old_recipe_sum_calories = deepcopy(recipe_record_with_products.summary_calories)

    # sanity check
    assert len(recipe_record_with_products.products_for_recipe) == 1
    assert old_recipe_sum_proteins == 102.22
    assert old_recipe_sum_fats == 56.78
    assert old_recipe_sum_carbohydrates == 85.46
    assert old_recipe_sum_calories == 141.96

    # when
    await recipe_service.add_product(
        id=recipe_record_with_products.id,
        user_id=recipe_record_with_products.user_id,
        input_dto=product_for_recipe_input
    )

    # then
    recipe = await recipe_service.get_by_id(recipe_record_with_products.id)

    assert len(recipe.products_for_recipe) == 2
    product_for_recipe = next(
        filter(lambda x: x.product_id == product_for_recipe_input.product_id, recipe.products_for_recipe)
    )

    assert product_for_recipe.product_id == product_record.id
    assert product_for_recipe.weight_in_grams == weight_in_grams
    assert product_for_recipe.carbohydrates == 24.11
    assert product_for_recipe.proteins == 48.22
    assert product_for_recipe.fats == 12.06
    assert product_for_recipe.calories == 120.56

    assert recipe.summary_proteins != old_recipe_sum_proteins
    assert recipe.summary_fats != old_recipe_sum_fats
    assert recipe.summary_carbohydrates != old_recipe_sum_carbohydrates
    assert recipe.summary_calories != old_recipe_sum_calories

    assert recipe.summary_proteins == 150.44
    assert recipe.summary_fats == 68.84
    assert recipe.summary_carbohydrates == 109.57
    assert recipe.summary_calories == 262.52


@pytest.mark.asyncio
async def test_recipe_service_add_product_to_recipe_not_found(recipe_record, product_record, recipe_service):
    # when/then
    with pytest.raises(RecipeNotFound):
        await recipe_service.add_product(
            id=uuid6(),
            user_id=recipe_record.user_id,
            input_dto=ProductForRecipeInputDto(
                product_id=product_record.id,
                weight_in_grams=100
            )
        )


@pytest.mark.asyncio
async def test_recipe_service_add_product_to_recipe_wrong_user(recipe_record, product_record, recipe_service):
    # when/then
    with pytest.raises(ProductForRecipeNotRecordOwner):
        await recipe_service.add_product(
            id=recipe_record.id,
            user_id=uuid6(),
            input_dto=ProductForRecipeInputDto(
                product_id=product_record.id,
                weight_in_grams=100
            )
        )


@pytest.mark.asyncio
async def test_recipe_service_update_product_in_recipe(recipe_record_with_products, recipe_service):
    # given
    recipe = await recipe_service.get_by_id(recipe_id=recipe_record_with_products.id)
    product_for_recipe_id = recipe.products_for_recipe[0].id
    product_id = recipe.products_for_recipe[0].product_id
    product_weight = recipe.products_for_recipe[0].weight_in_grams

    update_dto = ProductForRecipeUpdateDto(
        weight_in_grams=product_weight + 100
    )

    old_recipe_sum_proteins = deepcopy(recipe.summary_proteins)
    old_recipe_sum_fats = deepcopy(recipe.summary_fats)
    old_recipe_sum_carbohydrates = deepcopy(recipe.summary_carbohydrates)
    old_recipe_sum_calories = deepcopy(recipe.summary_calories)

    old_product_weight = deepcopy(recipe.products_for_recipe[0].weight_in_grams)
    old_product_proteins = deepcopy(recipe.products_for_recipe[0].proteins)
    old_product_fats = deepcopy(recipe.products_for_recipe[0].fats)
    old_product_carbohydrates = deepcopy(recipe.products_for_recipe[0].carbohydrates)

    # when
    recipe = await recipe_service.update_product(
        id=product_for_recipe_id,
        update_dto=update_dto,
        user_id=recipe_record_with_products.user_id,
    )

    # then
    assert len(recipe.products_for_recipe) == 1
    product_for_recipe = recipe.products_for_recipe[0]

    assert product_for_recipe.weight_in_grams != old_product_weight
    assert product_for_recipe.proteins != old_product_proteins
    assert product_for_recipe.fats != old_product_fats
    assert product_for_recipe.carbohydrates != old_product_carbohydrates

    assert recipe.summary_proteins != old_recipe_sum_proteins
    assert recipe.summary_fats != old_recipe_sum_fats
    assert recipe.summary_carbohydrates != old_recipe_sum_carbohydrates
    assert recipe.summary_calories != old_recipe_sum_calories

    assert product_for_recipe.weight_in_grams == update_dto.weight_in_grams

    assert product_for_recipe.fats == 79.0
    assert product_for_recipe.proteins == 142.22
    assert product_for_recipe.carbohydrates == 118.9
    assert product_for_recipe.calories == 197.51
    assert product_for_recipe.product_id == product_id

    assert recipe.summary_proteins == 142.22
    assert recipe.summary_fats == 79.0
    assert recipe.summary_carbohydrates == 118.9
    assert recipe.summary_calories == 197.51


@pytest.mark.asyncio
async def test_recipe_service_update_product_in_recipe_not_found(recipe_record_with_products, recipe_service):
    # given
    product_for_recipe_id = uuid6()
    update_dto = ProductForRecipeUpdateDto(
        weight_in_grams=100
    )

    # when/then
    with pytest.raises(ProductForRecipeNotFound):
        await recipe_service.update_product(
            id=product_for_recipe_id,
            update_dto=update_dto,
            user_id=recipe_record_with_products.user_id,
        )


@pytest.mark.asyncio
async def test_recipe_service_update_product_in_recipe_wrong_user(recipe_record_with_products, recipe_service):
    # given
    product_for_recipe_id = recipe_record_with_products.products_for_recipe[0].id
    update_dto = ProductForRecipeUpdateDto(
        weight_in_grams=100
    )

    # when/then
    with pytest.raises(ProductForRecipeNotRecordOwner):
        await recipe_service.update_product(
            id=product_for_recipe_id,
            update_dto=update_dto,
            user_id=uuid6(),
        )


@pytest.mark.asyncio
async def test_recipe_service_delete_product_from_recipe(recipe_record_with_products, recipe_service):
    # sanity check
    assert len(recipe_record_with_products.products_for_recipe) == 1
    assert recipe_record_with_products.summary_proteins != 0
    assert recipe_record_with_products.summary_fats != 0
    assert recipe_record_with_products.summary_carbohydrates != 0
    assert recipe_record_with_products.summary_calories != 0

    # when
    await recipe_service.delete_product(
        id=recipe_record_with_products.products_for_recipe[0].id,
        user_id=recipe_record_with_products.user_id
    )
    # then
    recipe = await recipe_service.get_by_id(recipe_id=recipe_record_with_products.id)

    assert len(recipe.products_for_recipe) == 0
    assert recipe.summary_proteins == 0
    assert recipe.summary_fats == 0
    assert recipe.summary_carbohydrates == 0
    assert recipe.summary_calories == 0


@pytest.mark.asyncio
async def test_recipe_service_delete_product_from_recipe_not_found(recipe_record_with_products, recipe_service):
    # given
    product_for_recipe_id = uuid6()

    # when/then
    with pytest.raises(ProductForRecipeNotFound):
        await recipe_service.delete_product(
            id=product_for_recipe_id,
            user_id=recipe_record_with_products.user_id
        )


@pytest.mark.asyncio
async def test_recipe_service_delete_product_from_recipe_wrong_user(recipe_record_with_products, recipe_service):
    # given
    product_for_recipe_id = recipe_record_with_products.products_for_recipe[0].id

    # when/then
    with pytest.raises(ProductForRecipeNotRecordOwner):
        await recipe_service.delete_product(
            id=product_for_recipe_id,
            user_id=uuid6()
        )
