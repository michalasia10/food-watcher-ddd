from src.core.infra.tortoiserepo import TortoiseRepo
from src.modules.product.domain.entity.daily_product import (
    DailyUserProduct as DailyUserProductEntity,
)
from src.modules.product.infra.model.daily_product import (
    DailyUserProduct as DailyUserProductModel,
)


class DailyUserProductTortoiseRepo(
    TortoiseRepo[DailyUserProductModel, DailyUserProductEntity]
):
    model = DailyUserProductModel
    entity = DailyUserProductEntity
