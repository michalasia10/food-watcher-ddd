from datetime import datetime
from typing import Any

from pydantic import BaseModel
from uuid6 import UUID

from src.modules.product_new.application.dto.product import ProductOutputDto
from src.modules.product_new.domain.enum import UserProductType


class DailyUserProductDto(BaseModel):
    product_id: UUID
    weight_in_grams: float
    type: UserProductType


class DailyUserProductInputDto(DailyUserProductDto):
    date: datetime


class DailyUserProductOutputDto(DailyUserProductDto):
    id: UUID
    product: ProductOutputDto
    calories: float
    proteins: float
    fats: float
    carbohydrates: float
    type: Any
