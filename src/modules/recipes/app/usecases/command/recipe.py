from abc import abstractmethod
from typing import NoReturn

from src.foundation.application.commands import CommandBase
from src.foundation.domain.value_objects import UUID
from src.modules.recipes.app.usecases.dtos.recipe import (
    RecipeInputDto,
    RecipeOutputDto,
    RecipeProductInputDto,
)
from src.modules.recipes.domain.value_objects import RecipeID, ProductRecipeID


class RecipeCommand(CommandBase):

    def delete(self, id: [UUID]):
        raise NotImplementedError

    @abstractmethod
    def create(self, entity: RecipeInputDto) -> NoReturn: ...

    @abstractmethod
    def update(self, id: RecipeID, recipe: RecipeInputDto) -> RecipeOutputDto:
        raise NotImplementedError


class RecipeProductCommand(CommandBase):

    @abstractmethod
    def delete(self, id: [UUID]):
        raise NotImplementedError

    def create(self, entity: RecipeInputDto) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    def update(
        self, id: ProductRecipeID, recipe: RecipeProductInputDto
    ) -> RecipeOutputDto: ...
