from dataclasses import dataclass, field

from foundation.domain.value_objects import UUID
from src.modules.recipes.domain.value_objects import RecipeID


@dataclass(frozen=True)
class ProductOutputDto:
    code: int
    name: str
    quantity: str | None
    id: UUID | None
    brand: str | None
    size: str | None
    groups: str | None
    category: str | None
    energy_kcal_100g: float


@dataclass(frozen=True)
class RecipeProductInputDto:
    weight_in_grams: float
    product_id: UUID


@dataclass(frozen=True)
class RecipeProductOutputDto(RecipeProductInputDto):
    product: ProductOutputDto
    id: UUID | None = None
    calories: float | None = None
    proteins: float | None = None
    fats: float | None = None
    carbohydrates: float | None = None


@dataclass(frozen=True)
class RecipeOutputDto:
    name: str
    id: RecipeID | None = None
    link: str | None = None
    description: str | None = None
    products: list[RecipeProductOutputDto] = field(default_factory=list)
    summary_calories: float | None = None
    summary_proteins: float | None = None
    summary_fats: float | None = None
    summary_carbohydrates: float | None = None


@dataclass(frozen=True)
class RecipeInputDto:
    name: str
    link: str | None = None
    description: str | None = None
    products: list[RecipeProductInputDto] = field(default_factory=list)
