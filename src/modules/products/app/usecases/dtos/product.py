from dataclasses import dataclass

from modules.products.domain.value_objects import ProductID


@dataclass(frozen=True)
class ProductOutputDto:
    id: ProductID
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
