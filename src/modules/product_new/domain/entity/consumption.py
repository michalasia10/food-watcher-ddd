from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from src.core_new.domain.entity import Entity
from src.core_new.domain.value_object import PrecisedFloat
from src.modules.common.macro.factory import MacroCalculatorType, MacroCalculatorFactory
from src.modules.common.macro.strategies import MacroCalculatorStrategy


@dataclass
class DailyUserConsumption(Entity):
    date: datetime
    user_id: UUID | None = None
    products: list['DailyUserProduct'] = field(default_factory=list)
    summary_proteins: PrecisedFloat = PrecisedFloat(.0)
    summary_fats: PrecisedFloat = PrecisedFloat(.0)
    summary_carbohydrates: PrecisedFloat = PrecisedFloat(.0)
    summary_calories: PrecisedFloat = PrecisedFloat(.0)

    @classmethod
    def create(cls, user_id: UUID) -> 'DailyUserConsumption':
        entity = cls(
            id=cls.create_id(),
            updated_at=cls.create_now_time(),
            created_at=cls.create_now_time(),
            user_id=user_id,
            date=cls.create_now_time(),
        )
        return entity

    def add_product(self, product: 'DailyUserProduct') -> None:
        """
        Method to calculate summary macros and calories for the daily user consumption entity based on the product.

        Args:
            product: `DailyUserProduct`

        Returns: None

        """
        macro: MacroCalculatorStrategy = MacroCalculatorFactory.create_strategy(
            strategy_type=MacroCalculatorType.SUMMARY_STRATEGY
        )
        macro.calculate(self, product)

    def delete_product(self, product: 'DailyUserProduct') -> None:
        """
        Method to subtract summary macros and calories for the daily user consumption entity based on the product.

        Args:
            product: `DailyUserProduct`

        Returns: None

        """

        macro: MacroCalculatorStrategy = MacroCalculatorFactory.create_strategy(
            strategy_type=MacroCalculatorType.SUBTRACT_STRATEGY
        )
        macro.calculate(self, product)
