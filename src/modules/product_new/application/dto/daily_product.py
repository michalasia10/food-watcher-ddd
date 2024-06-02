from datetime import datetime, date
from typing import Any

from pydantic import BaseModel
from uuid import UUID

from src.modules.product_new.application.dto.product import ProductOutputDto
from src.modules.product_new.domain.enum import UserProductType


class DailyUserProductDto(BaseModel):
    product_id: UUID
    weight_in_grams: float
    type: UserProductType


class DailyUserProductInputDto(DailyUserProductDto):
    date: datetime | date

    def model_post_init(self, __context: Any) -> None:
        """
        Method to reset datetime for hours,minutes,seconds and microseconds.
        """
        self.date = date(self.date.year, self.date.month, self.date.day)


class DailyUserProductOutputDto(DailyUserProductDto):
    id: UUID
    product: ProductOutputDto
    calories: float
    proteins: float
    fats: float
    carbohydrates: float
    type: Any
