from src.core.infra.repo.tortoiserepo import TortoiseRepo
from src.modules.recipe.domain.entity.recipe_product import (
    ProductForRecipe as ProductForRecipeEntity,
)
from src.modules.recipe.infra.model.recipe_product import (
    ProductForRecipe as ProductForRecipeModel,
)


class RecipeForProductTortoiseRepo(
    TortoiseRepo[ProductForRecipeModel, ProductForRecipeEntity]
):
    model = ProductForRecipeModel
    entity = ProductForRecipeEntity
