from src.core.infra.repo.tortoiserepo import TortoiseRepo
from src.modules.recipe.domain.entity.recipe import Recipe as RecipeEntity
from src.modules.recipe.infra.model.recipe import Recipe as RecipeModel


class RecipeTortoiseRepo(TortoiseRepo[RecipeModel, RecipeEntity]):
    model = RecipeModel
    entity = RecipeEntity
