from abc import abstractmethod
from typing import Any, NoReturn

from src.foundation.domain.repository import GenericRepository
from src.modules.products.domain.entities import Product
from src.modules.products.domain.value_objects import ProductID


class ProductRepository(GenericRepository):

    @abstractmethod
    def get_by_id(self, id: ProductID) -> Product:
        ...

    @abstractmethod
    def get_by_field_value(self, field: str, value: Any) -> Product:
        ...

    @abstractmethod
    def update(self, entity: Product) -> NoReturn:
        ...

    @abstractmethod
    def create(self, entity: Product) -> NoReturn:
        ...

    @abstractmethod
    def get_all(self) -> list[Product]:
        ...

    @abstractmethod
    def get_all_pagination(self, skip: int, limit: int) -> list[Product]:
        ...
