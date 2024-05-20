from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ProductInputDto(BaseModel):
    code: Optional[int]
    name: Optional[str]
    quantity: Optional[str]
    brand: Optional[str]
    size: Optional[str]
    groups: Optional[str]
    category: Optional[str]
    energy_kcal_100g: Optional[float]
    fat_100g: Optional[float]
    carbohydrates_100g: Optional[float]
    sugars_100g: Optional[float]
    proteins_100g: Optional[float]


class ProductOutputDto(ProductInputDto):
    id: UUID

