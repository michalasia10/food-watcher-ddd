from dataclasses import dataclass, field
from uuid import UUID

from src.core_new.domain.entity import Entity
from src.core_new.domain.value_object import PrecisedFloat
from src.modules.common.macro.factory import MacroCalculatorType, MacroCalculatorFactory
from src.modules.common.macro.strategies import MacroCalculatorStrategy
from src.modules.product_new.domain.entity.consumption import DailyUserConsumption
from src.modules.product_new.domain.entity.product import Product
from src.modules.product_new.domain.enum import UserProductType


@dataclass
class DailyUserProduct(Entity):
    product: Product | None = None
    day: DailyUserConsumption | None = None
    day_id: UUID | None = None
    product_id: UUID | None = None
    weight_in_grams: PrecisedFloat | None = None
    type: UserProductType = field(kw_only=True, default=UserProductType.LUNCH)
    calories: PrecisedFloat | None = None
    proteins: PrecisedFloat | None = None
    fats: PrecisedFloat | None = None
    carbohydrates: PrecisedFloat | None = None

    @classmethod
    def create(
            cls,
            product: Product,
            day: DailyUserConsumption,
            weight_in_grams: float | PrecisedFloat | None = None,
            type: UserProductType = UserProductType.LUNCH,
    ) -> 'DailyUserProduct':
        entity = cls(
            id=cls.create_id(),
            updated_at=cls.create_now_time(),
            created_at=cls.create_now_time(),
            product_id=product.id,
            day_id=day.id,
            weight_in_grams=PrecisedFloat(weight_in_grams),
            type=type,
        )
        entity.set_makros(product=product)
        day.add_product(product=entity)
        return entity

    def set_makros(self, product) -> None:
        """
        Method to set makros for based on product.

        Returns: None

        """
        macro: MacroCalculatorStrategy = MacroCalculatorFactory.create_strategy(
            strategy_type=MacroCalculatorType.WEIGHT_STRATEGY
        )
        macro.calculate(self, product)


