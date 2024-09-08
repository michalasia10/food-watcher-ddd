from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, model_validator

from src.modules.product.application.dto.daily_product import DailyUserProductOutputDto


class MacroDto(BaseModel):
    proteins: float | None
    fats: float | None
    carbs: float | None
    calories: float | None


class DailyUserConsumptionOutputDto(BaseModel):
    user_id: UUID
    date: datetime
    id: UUID
    products: list[DailyUserProductOutputDto] | None
    summary: MacroDto
    user: MacroDto

    @model_validator(mode="before")
    @classmethod
    def transform_data(cls, data: dict[str, Any]) -> dict[str, Any]:
        macro = {}

        for key, value in list(data.items()):
            if key.startswith("summary_"):
                macro_key = key.replace("summary_", "").replace("carbohydrates", "carbs")
                macro[macro_key] = value
                data.pop(key)

        data["summary"] = macro

        return data
