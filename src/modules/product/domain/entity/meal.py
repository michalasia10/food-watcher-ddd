from dataclasses import dataclass, field

from src.core.domain.value_object import PrecisedFloat
from src.modules.common.macro.factory import MacroCalculatorType, MacroCalculatorFactory
from src.modules.common.macro.strategies import MacroCalculatorStrategy
from src.modules.product.domain.enum import UserProductType


@dataclass
class Meal:
    type: UserProductType
    products: list["DailyUserProduct"] = field(default_factory=list)
    summary_proteins: PrecisedFloat = PrecisedFloat(0.0)
    summary_fats: PrecisedFloat = PrecisedFloat(0.0)
    summary_carbohydrates: PrecisedFloat = PrecisedFloat(0.0)
    summary_calories: PrecisedFloat = PrecisedFloat(0.0)

    def add_products(self, products: list["DailyUserProduct"]) -> None:
        """
        Method to calculate summary macros and calories for the meal based on the product.

        Args:
            products: `DailyUserProduct`

        Returns: None

        """
        macro: MacroCalculatorStrategy = MacroCalculatorFactory.create_strategy(
            strategy_type=MacroCalculatorType.SUMMARY_STRATEGY
        )
        for product in products:
            macro.calculate(self, product)
            self.products.append(product)
