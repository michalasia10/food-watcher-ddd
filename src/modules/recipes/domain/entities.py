from pydantic import Field
from pydantic.dataclasses import dataclass

from src.foundation.domain.entities import AggregateRoot
from src.modules.recipes.infra.models.recipe import Recipe as RecipeModel


@dataclass
class ProductRecipe(AggregateRoot):
    code: int | None = None
    name: str | None = None
    quantity: str | None = None
    brand: str | None = None
    size: str | None = None
    groups: str | None = None
    category: str | None = None
    energy_kcal_100g: float | None = None
    fat_100g: float | None = None
    carbohydrates_100g: float | None = None
    sugars_100g: float | None = None
    proteins_100g: float | None = None


@dataclass
class Recipe(AggregateRoot):
    name: str | None = None
    link: str | None = None
    description: str | None = None
    products: list[ProductRecipe] = Field(default_factory=list)

    class Meta:
        orm_model = RecipeModel
