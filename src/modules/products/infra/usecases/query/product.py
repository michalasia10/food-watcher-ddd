from foundation.domain.value_objects import UUID
from modules.products.domain.value_objects import ProductID
from src.modules.products.app.repository.product import ProductRepository
from src.modules.products.app.usecases.dtos.product import ProductOutputDto
from src.modules.products.app.usecases.query.product import ProductQuery as ProductQueryBase


class ProductQuery(ProductQueryBase):
    def __init__(self, repository: ProductRepository):
        self._repository = repository

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ProductOutputDto]:
        return [ProductOutputDto(**product.to_dict()) for product in self._repository.get_all_pagination(skip, limit)]

    def get_by_id(self, id: UUID) -> ProductOutputDto:
        user = self._repository.get_by_id(ProductID(id))
        return ProductOutputDto(**user.to_dict())
