from dataclasses import dataclass
import typing
from uuid import UUID

from src.core.domain.entity import Entity
from src.core.domain.value_object import PrecisedFloat
from src.modules.common.macro.factory import MacroCalculatorFactory, MacroCalculatorType
from src.modules.common.macro.strategies import MacroCalculatorStrategy

if typing.TYPE_CHECKING:
    from src.modules.recipe.domain.entity.recipe_product import ProductForRecipe


@dataclass
class Recipe(Entity):
    user_id: UUID
    name: str | None = None
    link: str | None = None
    description: str | None = None
    products_for_recipe: list["ProductForRecipe"] | None = None
    summary_calories: PrecisedFloat = PrecisedFloat(0.0)
    summary_proteins: PrecisedFloat = PrecisedFloat(0.0)
    summary_fats: PrecisedFloat = PrecisedFloat(0.0)
    summary_carbohydrates: PrecisedFloat = PrecisedFloat(0.0)

    @classmethod
    def create(
        cls, name: str, link: str, description: str, user_id: UUID
    ) -> ["Recipe"]:
        return cls(
            id=cls.create_id(),
            updated_at=cls.create_now_time(),
            created_at=cls.create_now_time(),
            name=name,
            link=link,
            description=description,
            user_id=user_id,
        )

    def add_product(self, product: "ProductForRecipe") -> None:
        macro: MacroCalculatorStrategy = MacroCalculatorFactory.create_strategy(
            MacroCalculatorType.SUMMARY_STRATEGY.value
        )
        macro.calculate(self, product)

    def delete_product(self, product: "ProductForRecipe") -> None:
        macro: MacroCalculatorStrategy = MacroCalculatorFactory.create_strategy(
            MacroCalculatorType.SUBTRACT_STRATEGY.value
        )
        macro.calculate(self, product)
