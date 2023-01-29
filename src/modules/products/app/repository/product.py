from abc import abstractmethod
from typing import Any, NoReturn

from foundation.domain.repository import GenericRepostirory
from modules.products.domain.entities import Product
from modules.products.domain.value_objects import ProductID


class ProductRepository(GenericRepostirory):

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
