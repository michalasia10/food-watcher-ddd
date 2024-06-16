from dataclasses import dataclass
from uuid import UUID

from src.core.domain.entity import Entity
from src.core.domain.value_object import PrecisedFloat
from src.modules.common.macro.factory import MacroCalculatorType, MacroCalculatorFactory
from src.modules.common.macro.strategies import MacroCalculatorStrategy


@dataclass
class Product:
    id: UUID
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
class ProductForRecipe(Entity):
    product: Product | None = None
    product_id: UUID | None = None
    recipe_id: UUID | None = None
    weight_in_grams: PrecisedFloat = PrecisedFloat(.0)
    calories: PrecisedFloat = PrecisedFloat(.0)
    proteins: PrecisedFloat = PrecisedFloat(.0)
    fats: PrecisedFloat = PrecisedFloat(.0)
    carbohydrates: PrecisedFloat = PrecisedFloat(.0)

    @classmethod
    def create(
            cls,
            product: Product,
            recipe: 'Recipe',
            weight_in_grams: float | PrecisedFloat = PrecisedFloat(.0)
    ) -> 'ProductForRecipe':
        entity = cls(
            id=cls.create_id(),
            updated_at=cls.create_now_time(),
            created_at=cls.create_now_time(),
            product_id=product.id,
            recipe_id=recipe.id,
            weight_in_grams=PrecisedFloat(weight_in_grams)
        )
        entity.calculate_macros(product)
        recipe.add_product(entity)
        return entity

    def calculate_macros(self, product=None) -> None:
        macro: MacroCalculatorStrategy = MacroCalculatorFactory.create_strategy(
            MacroCalculatorType.WEIGHT_STRATEGY.value
        )
        macro.calculate(self, product)

    def update_weight(
            self,
            recipe:'Recipe',
            weight: float | PrecisedFloat
    ) -> None:
        recipe.delete_product(self)

        self.weight_in_grams = PrecisedFloat(weight)
        self.calculate_macros(self.product)

        recipe.add_product(self)

        # cleanups
        self.recipe_id = None
        self.product_id = None
        self.product = None
