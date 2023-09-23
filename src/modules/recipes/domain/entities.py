from pydantic import Field
from pydantic.dataclasses import dataclass

from foundation.domain.repository import UUID
from src.foundation.domain.entities import AggregateRoot
from src.modules.common.macro.factory import MacroCalculatorFactory, MacroCalculatorType
from src.modules.common.macro.strategies import MacroCalculatorStrategy
from src.modules.recipes.infra.models.recipe import Recipe as RecipeModel, ProductForRecipe as ProductForRecipeModel


@dataclass
class Product(AggregateRoot):
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
class ProductRecipe(AggregateRoot):
    weight_in_grams: float | None = None
    product_id: UUID | None = None
    product: Product | None = None
    recipe_id: UUID | None = None
    recipe = None
    calories: float | None = None
    proteins: float | None = None
    fats: float | None = None
    carbohydrates: float | None = None

    class Meta:
        orm_model = ProductForRecipeModel

    def calculate_macros(self, product=None):
        _product = product or self.product
        macro: MacroCalculatorStrategy = MacroCalculatorFactory.create_strategy(
            MacroCalculatorType.WEIGHT_STRATEGY.value
        )
        macro.calculate(self, _product)


@dataclass
class Recipe(AggregateRoot):
    name: str | None = None
    link: str | None = None
    description: str | None = None
    products: list[ProductRecipe] = Field(default_factory=list)
    summary_calories: float | None = 0
    summary_proteins: float | None = 0
    summary_fats: float | None = 0
    summary_carbohydrates: float | None = 0

    class Meta:
        orm_model = RecipeModel

    def add_product(self, product: ProductRecipe):
        macro: MacroCalculatorStrategy = MacroCalculatorFactory.create_strategy(
            MacroCalculatorType.SUMMARY_STRATEGY.value
        )
        macro.calculate(self, product)

    def delete_product(self, product: ProductRecipe):
        self.products.remove(product)
        macro: MacroCalculatorStrategy = MacroCalculatorFactory.create_strategy(
            MacroCalculatorType.SUBTRACT_STRATEGY.value
        )
        macro.calculate(self, product)
