from abc import ABC

from src.foundation.domain.repository import GenericRepository
from src.modules.recipes.domain.entities import Recipe
from src.modules.recipes.domain.value_objects import RecipeID


class RecipeRepository(GenericRepository[Recipe, RecipeID], ABC):
    ...
