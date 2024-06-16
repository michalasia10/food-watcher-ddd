from uuid import UUID

from pydantic import Field, BaseModel

from src.modules.recipe_new.application.dto.recipe_product import ProductForRecipeInputDto, ProductForRecipeOutputDto


class RecipeOutputDto(BaseModel):
    id: UUID
    user_id: UUID
    name: str | None = None
    link: str | None = None
    description: str | None = None
    products_for_recipe: list[ProductForRecipeOutputDto] = Field(default_factory=list)
    summary_calories: float | None = None
    summary_proteins: float | None = None
    summary_fats: float | None = None
    summary_carbohydrates: float | None = None


class RecipeUpdateDto(BaseModel):
    name: str | None = None
    link: str | None = None
    description: str | None = None


class RecipeInputDto(RecipeUpdateDto):
    name: str
    products: list[ProductForRecipeInputDto | None] = Field(default_factory=list)
