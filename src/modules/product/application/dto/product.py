from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ProductInputDto(BaseModel):
    code: Optional[int] = None
    name: Optional[str] = None
    quantity: Optional[str] = None
    brand: Optional[str] = None
    size: Optional[str] = None
    groups: Optional[str] = None
    category: Optional[str] = None
    energy_kcal_100g: Optional[float] = None
    fat_100g: Optional[float] = None
    carbohydrates_100g: Optional[float] = None
    sugars_100g: Optional[float] = None
    proteins_100g: Optional[float] = None


class ProductOutputDto(ProductInputDto):
    id: UUID
