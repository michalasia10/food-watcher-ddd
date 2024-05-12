from abc import abstractmethod
from typing import NoReturn

from src.foundation.application.commands import CommandBase
from src.foundation.domain.value_objects import UUID
from src.modules.products.domain.value_objects import ProductID
from src.modules.products.app.usecases.dtos.product import (
    ProductOutputDto,
    ProductInputDto,
)


class ProductCommand(CommandBase):

    def delete(self, id: [UUID]):
        raise NotImplementedError

    @abstractmethod
    def create(self, entity: ProductInputDto) -> NoReturn: ...

    @abstractmethod
    def update(self, id: ProductID, user: ProductInputDto) -> ProductOutputDto: ...
