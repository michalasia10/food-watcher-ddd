from abc import abstractmethod

from modules.recipes.app.usecases.dtos.recipe import RecipeOutputDto
from src.foundation.application.queries import QueryBase


class RecipeQuery(QueryBase):
    @abstractmethod
    def get_all(self, skip: int, limit: int) -> list[RecipeOutputDto]: ...
