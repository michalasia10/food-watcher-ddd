from src.foundation.domain.value_objects import UUID
from src.modules.recipes.app.repository.recipe import RecipeRepository
from src.modules.recipes.app.usecases.dtos.recipe import RecipeOutputDto
from src.modules.recipes.app.usecases.query.recipe import RecipeQuery as RecipeQueryBase
from src.modules.recipes.domain.value_objects import RecipeID


class RecipeQuery(RecipeQueryBase):
    def __init__(self, repository: RecipeRepository):
        self._repository = repository

    def get_all(self, skip: int = 0, limit: int = 100) -> list[RecipeOutputDto]:
        return [
            RecipeOutputDto(**recipe.to_dict())
            for recipe in self._repository.get_all_pagination(skip, limit)
        ]

    def get_by_id(self, id: UUID) -> RecipeOutputDto:
        recipe = self._repository.get_by_id(RecipeID(id))
        return RecipeOutputDto(**recipe.to_dict())
