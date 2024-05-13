import dataclasses

from src.modules.products.app.usecases.dtos.product import (
    ProductInputDto,
    ProductOutputDto,
)
from src.modules.products.domain.exceptions import ProductAlreadyExists, ProductNotFound
from src.modules.products.domain.value_objects import ProductID
from src.modules.products.app.repository.product import ProductRepository
from src.modules.products.app.usecases.command.product import (
    ProductCommand as ProductCommandBase,
)
from src.modules.products.domain.entities import Product


class ProductCommand(ProductCommandBase):

    def __init__(self, repository: ProductRepository):
        self._repository = repository

    def create(self, product: ProductInputDto) -> ProductOutputDto:
        if self._repository.exists("code", product.code):
            raise ProductAlreadyExists("Product already exists.")
        product = self._repository.create(Product(**dataclasses.asdict(product)))
        return ProductOutputDto(**product.to_dict())

    def delete(self, id: ProductID):
        if not self._repository.exists("id", id):
            raise ProductNotFound("Product not found.")
        self._repository.delete(id)

    def update(self, id: ProductID, product: ProductInputDto) -> ProductOutputDto:
        return self._repository.update(Product(**dataclasses.asdict(product)))
