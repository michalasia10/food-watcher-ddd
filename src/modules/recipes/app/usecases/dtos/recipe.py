from dataclasses import dataclass, field

from foundation.domain.value_objects import UUID
from src.modules.recipes.domain.value_objects import RecipeID


@dataclass(frozen=True)
class ProductRecipeBaseDto:
    id: UUID


@dataclass(frozen=True)
class ProductRecipeOutputDto(ProductRecipeBaseDto):
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
class RecipeOutputDto:
    id: RecipeID
    name: str
    link: str | None = None
    description: str | None = None
    products: list[ProductRecipeOutputDto] = field(default_factory=list)


@dataclass(frozen=True)
class RecipeInputDto:
    name: str
    link: str | None = None
    description: str | None = None
    products: list[ProductRecipeBaseDto] = field(default_factory=list)
