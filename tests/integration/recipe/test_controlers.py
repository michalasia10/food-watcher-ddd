from http import HTTPStatus

import pytest
from tortoise.exceptions import DoesNotExist
from uuid6 import uuid6

from src.modules.recipe_new.application.dto.recipe import RecipeInputDto, RecipeUpdateDto
from src.modules.recipe_new.application.dto.recipe_product import ProductForRecipeInputDto, ProductForRecipeUpdateDto
from src.modules.recipe_new.infra.repo.recipe import RecipeTortoiseRepo
from src.modules.recipe_new.infra.repo.recipe_product import RecipeForProductTortoiseRepo


@pytest.mark.asyncio
async def test_recipe_controller_get_all_recipes(api_client, endpoint_enum, user_token, recipe_record):
    # given
    api_client.set_token(user_token.api_token)

    # when
    response = await api_client.get(endpoint_enum.RECIPE.value)

    # then
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()

    assert len(response_json) == 1
    api_client.compare_response_object_with_db(response_json[0], recipe_record)


@pytest.mark.asyncio
async def test_recipe_controller_get_all_recipes_with_products(
        api_client,
        endpoint_enum,
        user_token,
        recipe_record_with_products
):
    # given
    api_client.set_token(user_token.api_token)

    # when
    response = await api_client.get(endpoint_enum.RECIPE.value)

    # then
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()

    assert len(response_json) == 1
    assert len(response_json[0]['products_for_recipe']) == 1
    assert response_json[0]['products_for_recipe'][0]['product'] is not None

    api_client.compare_response_object_with_db(response_json[0], recipe_record_with_products)


@pytest.mark.asyncio
async def test_recipe_controller_get_recipe(api_client, endpoint_enum, user_token, recipe_record_with_products):
    # given
    api_client.set_token(user_token.api_token)

    # when
    response = await api_client.get(endpoint_enum.RECIPE.get_detail(recipe_record_with_products.id))

    # then
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()

    assert len(response_json['products_for_recipe']) == 1
    assert response_json['products_for_recipe'][0]['product'] is not None

    api_client.compare_response_object_with_db(response_json, recipe_record_with_products)


@pytest.mark.asyncio
async def test_recipe_controller_get_recipe_not_found(
        api_client,
        endpoint_enum,
        user_token,
        recipe_record_with_products
):
    # given
    api_client.set_token(user_token.api_token)

    # when
    response = await api_client.get(endpoint_enum.RECIPE.get_detail(uuid6()))

    # then
    api_client.check_status_code_in_error_response(response, HTTPStatus.NOT_FOUND)


@pytest.mark.asyncio
async def test_recipe_get_all_recipes_for_user(api_client, endpoint_enum, user_token, recipe_record_with_products):
    # given
    api_client.set_token(user_token.api_token)

    # when
    response = await api_client.get(endpoint_enum.RECIPE.get_detail('all_my_recipes'))

    # then
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()

    assert len(response_json) == 1
    assert len(response_json[0]['products_for_recipe']) == 1
    assert response_json[0]['products_for_recipe'][0]['product'] is not None

    api_client.compare_response_object_with_db(response_json[0], recipe_record_with_products)


@pytest.mark.asyncio
async def test_recipe_get_all_recipes_for_user_empty(api_client, endpoint_enum, user_token):
    # given
    api_client.set_token(user_token.api_token)

    # when
    response = await api_client.get(endpoint_enum.RECIPE.get_detail('all_my_recipes'))

    # then
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()

    assert len(response_json) == 0


@pytest.mark.asyncio
async def test_recipe_controller_create_recipe(api_client, endpoint_enum, user_token, product_record):
    # given
    api_client.set_token(user_token.api_token)
    weight_in_grams = 20.56
    name = 'recipe'
    recipe_input = RecipeInputDto(
        name=name,
        products=[
            ProductForRecipeInputDto(
                product_id=str(product_record.id),
                weight_in_grams=weight_in_grams,
            )
        ]
    )
    # when
    response = await api_client.post(endpoint_enum.RECIPE.value, json_data=recipe_input.dict())

    # then
    assert response.status_code == HTTPStatus.CREATED
    recipe_from_db = await RecipeTortoiseRepo.aget_first_from_filter(name=recipe_input.name)

    response_json = response.json()
    api_client.compare_response_object_with_db(response_json, recipe_from_db, recipe_input)


@pytest.mark.asyncio
async def test_recip_controller_create_recipe_with_empty_products(api_client, endpoint_enum, user_token):
    # given
    api_client.set_token(user_token.api_token)
    name = 'recipe'
    recipe_input = RecipeInputDto(
        name=name,
        products=[]
    )
    # when
    response = await api_client.post(endpoint_enum.RECIPE.value, json_data=recipe_input.dict())

    # then
    assert response.status_code == HTTPStatus.CREATED
    recipe_from_db = await RecipeTortoiseRepo.aget_first_from_filter(name=recipe_input.name)

    response_json = response.json()
    api_client.compare_response_object_with_db(response_json, recipe_from_db, recipe_input)


@pytest.mark.asyncio
async def test_recipe_controller_create_then_get(
        api_client,
        endpoint_enum,
        user_token,
        product_record
):
    # given
    api_client.set_token(user_token.api_token)
    weight_in_grams = 20.56
    name = 'recipe'
    recipe_input = RecipeInputDto(
        name=name,
        products=[
            ProductForRecipeInputDto(
                product_id=str(product_record.id),
                weight_in_grams=weight_in_grams,
            )
        ]
    )
    # when
    response = await api_client.post(endpoint_enum.RECIPE.value, json_data=recipe_input.dict())

    # then
    assert response.status_code == HTTPStatus.CREATED
    recipe_from_db = await RecipeTortoiseRepo.aget_first_from_filter(name=recipe_input.name)

    response_json = response.json()
    api_client.compare_response_object_with_db(response_json, recipe_from_db, recipe_input)

    # when
    response = await api_client.get(endpoint_enum.RECIPE.get_detail('all_my_recipes'))

    # then
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()

    assert len(response_json) == 1
    assert len(response_json[0]['products_for_recipe']) == 1
    assert response_json[0]['products_for_recipe'][0]['product'] is not None

    api_client.compare_response_object_with_db(response_json[0], recipe_from_db)


@pytest.mark.asyncio
async def test_recipe_controller_create_recipe_with_multiple_products(
        api_client,
        endpoint_enum,
        user_token,
        product_record,
        product_record2
):
    # given
    api_client.set_token(user_token.api_token)
    name = 'recipe'
    recipe_input = RecipeInputDto(
        name=name,
        products=[
            ProductForRecipeInputDto(
                product_id=str(product_record.id),
                weight_in_grams=22.55,
            ),
            ProductForRecipeInputDto(
                product_id=str(product_record2.id),
                weight_in_grams=33.33,
            )
        ]
    )
    # when
    response = await api_client.post(endpoint_enum.RECIPE.value, json_data=recipe_input.dict())

    # then
    assert response.status_code == HTTPStatus.CREATED
    recipe_from_db = await RecipeTortoiseRepo.aget_first_from_filter(name=recipe_input.name)

    response_json = response.json()
    api_client.compare_response_object_with_db(response_json, recipe_from_db, recipe_input)


@pytest.mark.asyncio
async def test_recipe_controller_create_recipe_with_invalid_product_id(api_client, endpoint_enum, user_token):
    # given
    api_client.set_token(user_token.api_token)
    name = 'recipe'
    recipe_input = RecipeInputDto(
        name=name,
        products=[
            ProductForRecipeInputDto(
                product_id=uuid6(),
                weight_in_grams=22.55,
            )
        ]
    )
    # when
    response = await api_client.post(endpoint_enum.RECIPE.value, json_data=recipe_input.dict())

    # then
    api_client.check_status_code_in_error_response(response, HTTPStatus.BAD_REQUEST)


@pytest.mark.asyncio
async def test_recipe_controller_update_recipe_name(api_client, endpoint_enum, user_token, recipe_record_with_products):
    # given
    api_client.set_token(user_token.api_token)
    recipe_id = recipe_record_with_products.id
    new_name = 'new_recipe'
    recipe_update_input = RecipeUpdateDto(
        name=new_name,
    )
    # when
    response = await api_client.put(endpoint_enum.RECIPE.get_detail(recipe_id), json_data=recipe_update_input.dict())

    # then
    assert response.status_code == HTTPStatus.OK
    recipe_from_db = await RecipeTortoiseRepo.aget_by_id(recipe_id)

    response_json = response.json()
    api_client.compare_response_object_with_db(response_json, recipe_from_db)


@pytest.mark.asyncio
async def test_recipe_controller_update_recipe_name_link_desc(
        api_client,
        endpoint_enum,
        user_token,
        recipe_record_with_products
):
    # given
    api_client.set_token(user_token.api_token)
    recipe_id = recipe_record_with_products.id
    new_name = 'new_recipe'
    new_link = 'new_link'
    new_description = 'new_description'
    recipe_update_input = RecipeUpdateDto(
        name=new_name,
        link=new_link,
        description=new_description
    )
    # when
    response = await api_client.put(endpoint_enum.RECIPE.get_detail(recipe_id), json_data=recipe_update_input.dict())

    # then
    assert response.status_code == HTTPStatus.OK
    recipe_from_db = await RecipeTortoiseRepo.aget_by_id(recipe_id)

    response_json = response.json()
    api_client.compare_response_object_with_db(response_json, recipe_from_db)


@pytest.mark.asyncio
async def test_recipe_controller_update_dummy_recipe(
        api_client,
        endpoint_enum,
        user_token,
        recipe_record_with_products
):
    # given
    api_client.set_token(user_token.api_token)
    new_name = 'new_recipe'
    new_link = 'new_link'
    new_description = 'new_description'
    recipe_update_input = RecipeUpdateDto(
        name=new_name,
        link=new_link,
        description=new_description
    )
    # when
    response = await api_client.put(endpoint_enum.RECIPE.get_detail(uuid6()), json_data=recipe_update_input.dict())

    # then
    api_client.check_status_code_in_error_response(response, HTTPStatus.NOT_FOUND)


@pytest.mark.asyncio
async def test_recipe_controller_update_recipe_dummy_user(
        api_client,
        endpoint_enum,
        user_token,
        recipe_record_with_products
):
    # given
    api_client.set_token(uuid6())
    new_name = 'new_recipe'
    new_link = 'new_link'
    new_description = 'new_description'
    recipe_update_input = RecipeUpdateDto(
        name=new_name,
        link=new_link,
        description=new_description
    )
    # when
    response = await api_client.put(
        endpoint_enum.RECIPE.get_detail(recipe_record_with_products.id),
        json_data=recipe_update_input.dict()
    )

    # then
    api_client.check_status_code_in_error_response(response, HTTPStatus.UNAUTHORIZED)


@pytest.mark.asyncio
async def test_recipe_controller_update_recipe_user_not_owner(
        api_client,
        endpoint_enum,
        user_token,
        recipe_record_with_products,
        user_token2
):
    # given
    api_client.set_token(user_token2.api_token)
    new_name = 'new_recipe'
    new_link = 'new_link'
    new_description = 'new_description'
    recipe_update_input = RecipeUpdateDto(
        name=new_name,
        link=new_link,
        description=new_description
    )
    # when
    response = await api_client.put(
        endpoint_enum.RECIPE.get_detail(recipe_record_with_products.id),
        json_data=recipe_update_input.dict()
    )
    # then
    api_client.check_status_code_in_error_response(response, HTTPStatus.FORBIDDEN)


@pytest.mark.asyncio
async def test_recipe_controller_delete(
        api_client,
        endpoint_enum,
        user_token,
        recipe_record_with_products
):
    # given
    api_client.set_token(user_token.api_token)
    recipe_id = recipe_record_with_products.id

    # when
    response = await api_client.delete(endpoint_enum.RECIPE.get_detail(recipe_id))

    # then
    assert response.status_code == HTTPStatus.NO_CONTENT
    with pytest.raises(DoesNotExist):
        await RecipeTortoiseRepo.aget_by_id(recipe_id)


@pytest.mark.asyncio
async def test_recipe_controller_delete_dummy_recipe(
        api_client,
        endpoint_enum,
        user_token,
        recipe_record_with_products
):
    # given
    api_client.set_token(user_token.api_token)

    # when
    response = await api_client.delete(endpoint_enum.RECIPE.get_detail(uuid6()))

    # then
    api_client.check_status_code_in_error_response(response, HTTPStatus.NOT_FOUND)


@pytest.mark.asyncio
async def test_recipe_controller_delete_dummy_user(
        api_client,
        endpoint_enum,
        user_token,
        recipe_record_with_products
):
    # given
    api_client.set_token(uuid6())

    # when
    response = await api_client.delete(endpoint_enum.RECIPE.get_detail(recipe_record_with_products.id))

    # then
    api_client.check_status_code_in_error_response(response, HTTPStatus.UNAUTHORIZED)


@pytest.mark.asyncio
async def test_recipe_controller_delete_user_not_owner(
        api_client,
        endpoint_enum,
        user_token,
        recipe_record_with_products,
        user_token2
):
    # given
    api_client.set_token(user_token2.api_token)

    # when
    response = await api_client.delete(endpoint_enum.RECIPE.get_detail(recipe_record_with_products.id))

    # then
    api_client.check_status_code_in_error_response(response, HTTPStatus.FORBIDDEN)


@pytest.mark.asyncio
async def test_recipe_controller_add_product(
        api_client,
        endpoint_enum,
        user_token,
        recipe_record_with_products,
        product_record
):
    # given
    api_client.set_token(user_token.api_token)
    input_dto = ProductForRecipeInputDto(
        product_id=product_record.id,
        weight_in_grams=22.55
    )

    # sanity check
    assert len(recipe_record_with_products.products_for_recipe) == 1

    # when
    response = await api_client.post(
        endpoint_enum.RECIPE.get_detail(f'product_for_recipe/{recipe_record_with_products.id}'),
        json_data=input_dto.dict()
    )

    # then
    assert response.status_code == HTTPStatus.OK
    recipe_from_db = await RecipeTortoiseRepo.aget_by_id(
        recipe_record_with_products.id,
        fetch_fields=['products_for_recipe']
    )
    assert len(recipe_from_db.products_for_recipe) == 2
    api_client.compare_response_object_with_db(response.json(), recipe_from_db)


@pytest.mark.asyncio
async def test_recipe_controller_add_product_dummy_new_product_id(
        api_client,
        endpoint_enum,
        user_token,
        recipe_record_with_products
):
    # given
    api_client.set_token(user_token.api_token)
    input_dto = ProductForRecipeInputDto(
        product_id=uuid6(),
        weight_in_grams=22.55
    )

    # sanity check
    assert len(recipe_record_with_products.products_for_recipe) == 1

    # when
    response = await api_client.post(
        endpoint_enum.RECIPE.get_detail(f'product_for_recipe/{recipe_record_with_products.id}'),
        json_data=input_dto.dict()
    )

    # then
    api_client.check_status_code_in_error_response(response, HTTPStatus.BAD_REQUEST)


@pytest.mark.asyncio
async def test_recipe_controller_add_product_dummy_recipe_id(
        api_client,
        endpoint_enum,
        user_token,
        product_record
):
    # given
    api_client.set_token(user_token.api_token)
    input_dto = ProductForRecipeInputDto(
        product_id=product_record.id,
        weight_in_grams=22.55
    )

    # when
    response = await api_client.post(
        endpoint_enum.RECIPE.get_detail(f'product_for_recipe/{uuid6()}'),
        json_data=input_dto.dict()
    )

    # then
    api_client.check_status_code_in_error_response(response, HTTPStatus.NOT_FOUND)


@pytest.mark.asyncio
async def test_recipe_controller_add_product_dummy_user(
        api_client,
        endpoint_enum,
        user_token,
        recipe_record_with_products,
        product_record
):
    # given
    api_client.set_token(uuid6())
    input_dto = ProductForRecipeInputDto(
        product_id=product_record.id,
        weight_in_grams=22.55
    )

    # when
    response = await api_client.post(
        endpoint_enum.RECIPE.get_detail(f'product_for_recipe/{recipe_record_with_products.id}'),
        json_data=input_dto.dict()
    )

    # then
    api_client.check_status_code_in_error_response(response, HTTPStatus.UNAUTHORIZED)


@pytest.mark.asyncio
async def test_recipe_controller_add_product_user_not_owner(
        api_client,
        endpoint_enum,
        user_token,
        recipe_record_with_products,
        product_record,
        user_token2
):
    # given
    api_client.set_token(user_token2.api_token)
    input_dto = ProductForRecipeInputDto(
        product_id=product_record.id,
        weight_in_grams=22.55
    )

    # when
    response = await api_client.post(
        endpoint_enum.RECIPE.get_detail(f'product_for_recipe/{recipe_record_with_products.id}'),
        json_data=input_dto.dict()
    )

    # then
    api_client.check_status_code_in_error_response(response, HTTPStatus.FORBIDDEN)


@pytest.mark.asyncio
async def test_recipe_controller_update_product_for_recipe(
        api_client,
        endpoint_enum,
        user_token,
        recipe_record_with_products
):
    # given
    api_client.set_token(user_token.api_token)
    product_for_recipe_record = recipe_record_with_products.products_for_recipe[0]
    input_dto = ProductForRecipeUpdateDto(
        weight_in_grams=22.55
    )

    # when
    response = await api_client.put(
        endpoint_enum.RECIPE.get_detail(f'product_for_recipe/{product_for_recipe_record.id}'),
        json_data=input_dto.dict()
    )

    # then
    assert response.status_code == HTTPStatus.OK
    product_for_recipe_from_db = await RecipeForProductTortoiseRepo.aget_by_id(product_for_recipe_record.id)
    recipe_from_db = await RecipeTortoiseRepo.aget_by_id(
        recipe_record_with_products.id,
        fetch_fields=['products_for_recipe']
    )

    assert product_for_recipe_from_db.weight_in_grams == input_dto.weight_in_grams
    api_client.compare_response_object_with_db(response.json(), recipe_from_db)


@pytest.mark.asyncio
async def test_recipe_controller_update_product_dummy_id(
        api_client,
        endpoint_enum,
        user_token
):
    # given
    api_client.set_token(user_token.api_token)
    input_dto = ProductForRecipeUpdateDto(
        weight_in_grams=22.55
    )

    # when
    response = await api_client.put(
        endpoint_enum.RECIPE.get_detail(f'product_for_recipe/{uuid6()}'),
        json_data=input_dto.dict()
    )

    # then
    api_client.check_status_code_in_error_response(response, HTTPStatus.NOT_FOUND)


@pytest.mark.asyncio
async def test_recipe_controller_update_product_dummy_user(
        api_client,
        endpoint_enum,
        user_token,
        recipe_record_with_products
):
    # given
    api_client.set_token(uuid6())
    product_for_recipe_record = recipe_record_with_products.products_for_recipe[0]
    input_dto = ProductForRecipeUpdateDto(
        weight_in_grams=22.55
    )

    # when
    response = await api_client.put(
        endpoint_enum.RECIPE.get_detail(f'product_for_recipe/{product_for_recipe_record.id}'),
        json_data=input_dto.dict()
    )

    # then
    api_client.check_status_code_in_error_response(response, HTTPStatus.UNAUTHORIZED)


@pytest.mark.asyncio
async def test_recipe_controller_update_product_user_not_owner(
        api_client,
        endpoint_enum,
        user_token,
        recipe_record_with_products,
        user_token2
):
    # given
    api_client.set_token(user_token2.api_token)
    product_for_recipe_record = recipe_record_with_products.products_for_recipe[0]
    input_dto = ProductForRecipeUpdateDto(
        weight_in_grams=22.55
    )

    # when
    response = await api_client.put(
        endpoint_enum.RECIPE.get_detail(f'product_for_recipe/{product_for_recipe_record.id}'),
        json_data=input_dto.dict()
    )

    # then
    api_client.check_status_code_in_error_response(response, HTTPStatus.FORBIDDEN)


@pytest.mark.asyncio
async def test_recipe_controller_delete_product_for_recipe(
        api_client,
        endpoint_enum,
        user_token,
        recipe_record_with_products
):
    # given
    api_client.set_token(user_token.api_token)
    product_for_recipe_record = recipe_record_with_products.products_for_recipe[0]

    # when
    response = await api_client.delete(
        endpoint_enum.RECIPE.get_detail(f'product_for_recipe/{product_for_recipe_record.id}')
    )

    # then
    assert response.status_code == HTTPStatus.NO_CONTENT
    with pytest.raises(DoesNotExist):
        await RecipeForProductTortoiseRepo.aget_by_id(product_for_recipe_record.id)


@pytest.mark.asyncio
async def test_recipe_controller_delete_product_dummy_id(
        api_client,
        endpoint_enum,
        user_token
):
    # given
    api_client.set_token(user_token.api_token)

    # when
    response = await api_client.delete(
        endpoint_enum.RECIPE.get_detail(f'product_for_recipe/{uuid6()}')
    )

    # then
    api_client.check_status_code_in_error_response(response, HTTPStatus.NOT_FOUND)


@pytest.mark.asyncio
async def test_recipe_controller_delete_product_dummy_user(
        api_client,
        endpoint_enum,
        user_token,
        recipe_record_with_products
):
    # given
    api_client.set_token(uuid6())
    product_for_recipe_record = recipe_record_with_products.products_for_recipe[0]

    # when
    response = await api_client.delete(
        endpoint_enum.RECIPE.get_detail(f'product_for_recipe/{product_for_recipe_record.id}')
    )

    # then
    api_client.check_status_code_in_error_response(response, HTTPStatus.UNAUTHORIZED)


@pytest.mark.asyncio
async def test_recipe_controller_delete_product_user_not_owner(
        api_client,
        endpoint_enum,
        user_token,
        recipe_record_with_products,
        user_token2
):
    # given
    api_client.set_token(user_token2.api_token)
    product_for_recipe_record = recipe_record_with_products.products_for_recipe[0]

    # when
    response = await api_client.delete(
        endpoint_enum.RECIPE.get_detail(f'product_for_recipe/{product_for_recipe_record.id}')
    )

    # then
    api_client.check_status_code_in_error_response(response, HTTPStatus.FORBIDDEN)
