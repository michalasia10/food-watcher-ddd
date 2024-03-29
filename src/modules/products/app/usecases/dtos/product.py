from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Any

from modules.auth.domain.value_objects import UserID
from src.modules.products.domain.value_objects import ProductID, DailyUserProductID


@dataclass(frozen=True)
class ProductBaseDto:
    code: int
    name: str
    quantity: str | None
    brand: str | None
    size: str | None
    groups: str | None
    category: str | None
    energy_kcal_100g: float
    fat_100g: float | None
    carbohydrates_100g: float | None
    sugars_100g: float | None
    proteins_100g: float | None


@dataclass(frozen=True)
class ProductOutputDto(ProductBaseDto):
    id: ProductID


@dataclass(frozen=True)
class ProductInputDto(ProductBaseDto):
    ...


@dataclass(frozen=True)
class DailyUserProductDto:
    product_id: ProductID
    weight_in_grams: float
    type: Literal[1, 2]


@dataclass(frozen=True)
class DailyUserProductInputDto(DailyUserProductDto):
    user_id: UserID
    date: datetime


@dataclass(frozen=True)
class DailyUserProductOutputDto(DailyUserProductDto):
    id: DailyUserProductID
    calories: float
    proteins: float
    fats: float
    carbohydrates: float
    type: Any


@dataclass(frozen=True)
class DailyUserConsumptionOutputDto:
    user_id: UserID
    date: datetime
    products: list[DailyUserProductOutputDto] | None
    summary_calories: float | None
    summary_proteins: float | None
    summary_fats: float | None
    summary_carbohydrates: float | None
