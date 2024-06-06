from src.core_new.infra.tortoiserepo import TortoiseRepo
from src.modules.product_new.domain.entity.daily_product import DailyUserProduct as DailyUserProductEntity
from src.modules.product_new.infra.model.daily_product import DailyUserProduct as DailyUserProductModel


class DailyUserProductTortoiseRepo(TortoiseRepo[DailyUserProductModel, DailyUserProductEntity]):
    model = DailyUserProductModel
    entity = DailyUserProductEntity
