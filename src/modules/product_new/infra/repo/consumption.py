from src.core_new.infra.tortoiserepo import TortoiseRepo
from src.modules.product_new.domain.entity.consumption import DailyUserConsumption as DailyUserConsumptionEntity
from src.modules.product_new.infra.model.consumption import DailyUserConsumption as DailyUserConsumptionModel


class DailyUserConsumptionTortoiseRepo(TortoiseRepo[DailyUserConsumptionModel, DailyUserConsumptionEntity]):
    model = DailyUserConsumptionModel
    entity = DailyUserConsumptionEntity
