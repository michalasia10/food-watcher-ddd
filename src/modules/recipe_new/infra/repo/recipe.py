from src.core_new.infra.tortoiserepo import TortoiseRepo
from src.modules.recipe_new.domain.entity.recipe import Recipe as RecipeEntity
from src.modules.recipe_new.infra.model.recipe import Recipe as RecipeModel


class RecipeTortoiseRepo(TortoiseRepo[RecipeModel, RecipeEntity]):
    model = RecipeModel
    entity = RecipeEntity
