from src.modules.recipes.app.usecases.dtos.recipe import RecipeInputDto, ProductRecipeBaseDto
from src.modules.recipes.infra.usecases.command.recipe import RecipeCommand
from src.modules.recipes.app.repository.recipe import RecipeRepository

from tests.conftest import base_user_fix, commit_repos, db_session, product_fix, recipe_repo, product_repo


def test_command_create_recipe(recipe_repo: RecipeRepository, product_repo, product_fix):
    command = RecipeCommand(recipe_repo, product_repo)
    recipe_dto = RecipeInputDto(
        name="test",
        description="test",
        link="test",
        products=[ProductRecipeBaseDto(id=product_fix.id)]
    )
    command.create(recipe_dto)
    commit_repos([product_repo, recipe_repo])
    assert recipe_repo.exists('name', recipe_dto.name), "Recipe not found"
    recipe = recipe_repo.get_by_field_value('name', recipe_dto.name,raw=True)
    assert recipe.name == recipe_dto.name, "Recipe name not match"
    assert recipe.description == recipe_dto.description, "Recipe description not match"
    assert recipe.link == recipe_dto.link, "Recipe link not match"
    assert str(recipe.products[0].id) == str(recipe_dto.products[0].id), "Recipe product not match"
