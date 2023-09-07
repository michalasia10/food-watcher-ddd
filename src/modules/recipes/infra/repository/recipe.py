from src.foundation.infra.repository import Repository
from src.modules.recipes.app.repository.recipe import RecipeRepository
from src.modules.recipes.domain.entities import Recipe
from src.modules.recipes.domain.value_objects import RecipeID
from src.modules.recipes.infra.models.recipe import Recipe as RecipeModel


class SqlRecipeRepository(Repository[Recipe, RecipeID], RecipeRepository):
    model = RecipeModel
    entity = Recipe
