from datetime import datetime

from pydantic import BaseModel
from uuid6 import UUID

from src.modules.product_new.application.dto.daily_product import DailyUserProductOutputDto


class DailyUserConsumptionOutputDto(BaseModel):
    user_id: UUID
    date: datetime
    id: UUID
    products: list[DailyUserProductOutputDto] | None
    summary_calories: float | None
    summary_proteins: float | None
    summary_fats: float | None
    summary_carbohydrates: float | None
