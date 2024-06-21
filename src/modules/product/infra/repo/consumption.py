from src.core.infra.tortoiserepo import TortoiseRepo
from src.modules.product.domain.entity.consumption import (
    DailyUserConsumption as DailyUserConsumptionEntity,
)
from src.modules.product.infra.model.consumption import (
    DailyUserConsumption as DailyUserConsumptionModel,
)


class DailyUserConsumptionTortoiseRepo(
    TortoiseRepo[DailyUserConsumptionModel, DailyUserConsumptionEntity]
):
    model = DailyUserConsumptionModel
    entity = DailyUserConsumptionEntity
