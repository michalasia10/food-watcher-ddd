from abc import ABC

from src.foundation.domain.repository import GenericRepository
from src.modules.products.domain.entities import Product, DailyUserProduct, DailyUserConsumption
from src.modules.products.domain.value_objects import ProductID, DailyUserProductID, DailyUserConsID


class ProductRepository(GenericRepository[Product, ProductID], ABC):
    ...


class DailyUserProductRepository(GenericRepository[DailyUserProduct, DailyUserProductID], ABC):
    ...


class DailyUserConsumptionRepository(GenericRepository[DailyUserConsumption, DailyUserConsID], ABC):
    ...
