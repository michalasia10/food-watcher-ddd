from src.core_new.infra.tortoiserepo import TortoiseRepo
from src.modules.recipe_new.domain.entity.recipe_product import ProductForRecipe as ProductForRecipeEntity
from src.modules.recipe_new.infra.model.recipe_product import ProductForRecipe as ProductForRecipeModel


class RecipeForProductTortoiseRepo(TortoiseRepo[ProductForRecipeModel, ProductForRecipeEntity]):
    model = ProductForRecipeModel
    entity = ProductForRecipeEntity
