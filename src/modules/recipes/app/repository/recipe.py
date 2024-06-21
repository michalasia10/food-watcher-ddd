from abc import ABC

from src.foundation.domain.repository import GenericRepository
from src.modules.recipes.domain.entities import Recipe, ProductRecipe
from src.modules.recipes.domain.value_objects import RecipeID, ProductRecipeID


class RecipeRepository(GenericRepository[Recipe, RecipeID], ABC):
    ...


class ProductRecipeRepository(GenericRepository[ProductRecipe, ProductRecipeID], ABC):
    ...
