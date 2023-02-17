from pydantic.dataclasses import dataclass

from foundation.domain.entities import AggregateRoot
from modules.products.domain.value_objects import ProductID


@dataclass(kw_only=True)
class Product(AggregateRoot):
    id: ProductID
    code: int
    name: str
    quantity: str | None
    brand: str | None
    size: str | None
    groups: str | None
    category: str | None
    energy_kcal_100g: float | None
    fat_100g: float | None
    carbohydrates_100g: float | None
    sugars_100g: float | None
    proteins_100g: float | None
