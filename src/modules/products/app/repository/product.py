from abc import ABC, abstractmethod

from src.foundation.domain.repository import GenericRepository, Entity
from src.modules.products.domain.entities import (
    Product,
    DailyUserProduct,
    DailyUserConsumption,
)
from src.modules.products.domain.value_objects import (
    ProductID,
    DailyUserProductID,
    DailyUserConsID,
)


class ProductRepository(GenericRepository[Product, ProductID], ABC):

    @abstractmethod
    def get_all_by_name(self, name=None, skip=0, limit=10) -> list[Entity]: ...


class DailyUserProductRepository(
    GenericRepository[DailyUserProduct, DailyUserProductID], ABC
): ...


class DailyUserConsumptionRepository(
    GenericRepository[DailyUserConsumption, DailyUserConsID], ABC
): ...
