from src.foundation.infra.repository import Repository, Entity
from src.modules.products.app.repository.product import (
    ProductRepository,
    DailyUserProductRepository,
    DailyUserConsumptionRepository
)
from src.modules.products.domain.entities import Product, DailyUserConsumption, DailyUserProduct
from src.modules.products.domain.value_objects import ProductID, DailyUserProductID, DailyUserConsID
from src.modules.products.infra.models.product import (
    Product as ProductModel,
    DailyUserProducts as DailyUserProductModel,
    DailyUserConsumption as DailyUserConsumptionModel
)


class SqlProductRepository(Repository[Product, ProductID], ProductRepository):
    model = ProductModel
    entity = Product


class SqlDailyUserProductRepository(Repository[DailyUserProduct, DailyUserProductID], DailyUserProductRepository):
    model = DailyUserProductModel
    entity = DailyUserProduct


class SqlDailyUserConsumptionRepository(Repository[DailyUserConsumption, DailyUserConsID],
                                        DailyUserConsumptionRepository):
    model = DailyUserConsumptionModel
    entity = DailyUserConsumption
