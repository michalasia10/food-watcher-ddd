from src.foundation.infra.repository import Repository, Entity
from src.modules.products.app.repository.product import (
    ProductRepository,
    DailyUserProductRepository,
    DailyUserConsumptionRepository,
)
from src.modules.products.domain.entities import (
    Product,
    DailyUserConsumption,
    DailyUserProduct,
)
from src.modules.products.domain.value_objects import (
    ProductID,
    DailyUserProductID,
    DailyUserConsID,
)
from src.modules.products.infra.models.product import (
    Product as ProductModel,
    DailyUserProducts as DailyUserProductModel,
    DailyUserConsumption as DailyUserConsumptionModel,
)


class SqlProductRepository():
    pass
    # model = ProductModel
    # entity = Product
    #
    # def get_all_by_name(self, skip=0, limit=10, name=None) -> list[Entity]:
    #     if name:
    #         data = (
    #             self.session.query(self.model)
    #             .filter(self.model.name.like(f"%{name}%"))
    #             .limit(limit)
    #             .offset(skip)
    #             .all()
    #         )
    #         return [self.data_to_entity(dat, self.entity) for dat in data]
    #     else:
    #         return self.get_all_pagination(skip, limit)


class SqlDailyUserProductRepository():
    pass
#     Repository[DailyUserProduct, DailyUserProductID], DailyUserProductRepository
# ):
#     model = DailyUserProductModel
#     entity = DailyUserProduct
#

class SqlDailyUserConsumptionRepository():
    pass
#     Repository[DailyUserConsumption, DailyUserConsID], DailyUserConsumptionRepository
# ):
#     model = DailyUserConsumptionModel
#     entity = DailyUserConsumption
