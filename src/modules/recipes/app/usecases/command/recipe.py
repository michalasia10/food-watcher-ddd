from abc import abstractmethod
from typing import NoReturn

from src.foundation.application.commands import CommandBase
from src.foundation.domain.value_objects import UUID
from src.modules.recipes.app.usecases.dtos.recipe import RecipeInputDto, RecipeOutputDto
from src.modules.recipes.domain.value_objects import RecipeID


class RecipeCommand(CommandBase):

    def delete(self, id: [UUID]):
        raise NotImplementedError

    @abstractmethod
    def create(self, entity: RecipeInputDto) -> NoReturn:
        ...

    @abstractmethod
    def update(self, id: RecipeID, recipe: RecipeInputDto) -> RecipeOutputDto:
        raise NotImplementedError
