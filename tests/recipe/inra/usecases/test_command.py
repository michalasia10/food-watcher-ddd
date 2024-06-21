from copy import deepcopy

from src.modules.recipes.app.usecases.dtos.recipe import RecipeInputDto, RecipeProductInputDto
from src.modules.recipes.infra.usecases.command.recipe import RecipeCommand
from src.modules.recipes.app.repository.recipe import RecipeRepository

from tests.conftest import base_user_fix, commit_repos, db_session, product_fix, recipe_repo, product_repo, \
    recipe_product_repo


def test_command_create_recipe(recipe_repo: RecipeRepository, recipe_product_repo, product_repo, product_fix):
    command = RecipeCommand(recipe_repo, recipe_product_repo, product_repo, )
    recipe_dto = RecipeInputDto(
        name="test",
        description="test",
        link="test",
        products=[RecipeProductInputDto(product_id=product_fix.id, weight_in_grams=100)]
    )
    command.create(recipe_dto)
    commit_repos([product_repo, recipe_repo])
    assert recipe_repo.exists('name', recipe_dto.name), "Recipe not found"
    recipe = recipe_repo.get_by_field_value('name', recipe_dto.name, raw=True)
    assert recipe.name == recipe_dto.name, "Recipe name not match"
    assert recipe.description == recipe_dto.description, "Recipe description not match"
    assert recipe.link == recipe_dto.link, "Recipe link not match"
    recipe_product = deepcopy(recipe.products[0])
    expected_product = deepcopy(recipe_dto.products[0])
    assert str(recipe_product.product_id) == str(expected_product.product_id), "Recipe product not match"

    assert recipe.summary_calories
    assert recipe.summary_proteins
    assert recipe.summary_fats
    assert recipe.summary_carbohydrates
    assert recipe_product.calories
    assert recipe_product.proteins
    assert recipe_product.fats
    assert recipe_product.carbohydrates
    assert recipe_product.weight_in_grams == expected_product.weight_in_grams
