from uuid import UUID

from pydantic import BaseModel


class ProductOutputDto(BaseModel):
    code: int
    name: str
    quantity: str | None
    id: UUID | None
    brand: str | None
    size: str | None
    groups: str | None
    category: str | None
    energy_kcal_100g: float


class ProductForRecipeUpdateDto(BaseModel):
    weight_in_grams: float


class ProductForRecipeInputDto(ProductForRecipeUpdateDto):
    product_id: UUID


class ProductForRecipeOutputDto(ProductForRecipeInputDto):
    product: ProductOutputDto
    id: UUID | None = None
    calories: float | None = None
    proteins: float | None = None
    fats: float | None = None
    carbohydrates: float | None = None
