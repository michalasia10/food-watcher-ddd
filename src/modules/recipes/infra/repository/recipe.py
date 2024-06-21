from src.foundation.infra.repository import Repository
from src.modules.recipes.app.repository.recipe import RecipeRepository
from src.modules.recipes.domain.entities import Recipe, ProductRecipe
from src.modules.recipes.domain.value_objects import RecipeID, ProductRecipeID
from src.modules.recipes.infra.models.recipe import (
    Recipe as RecipeModel,
    ProductForRecipe as ProductForRecipeModel,
)


class SqlRecipeRepository(Repository[Recipe, RecipeID], RecipeRepository):
    model = RecipeModel
    entity = Recipe


class SqlRecipeProductRepository(
    Repository[ProductRecipe, ProductRecipeID],
):
    model = ProductForRecipeModel
    entity = ProductRecipe
