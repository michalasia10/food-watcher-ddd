from dataclasses import dataclass, field
from uuid import UUID

from modules.common.macro.factory import MacroCalculatorType, MacroCalculatorFactory
from modules.common.macro.strategies import MacroCalculatorStrategy
from src.core_new.domain.entity import Entity
from src.modules.product_new.domain.entity.consumption import DailyUserConsumption
from src.modules.product_new.domain.entity.product import Product
from src.modules.product_new.domain.enum import UserProductType


@dataclass
class DailyUserProduct(Entity):
    product: Product | None = None
    day: DailyUserConsumption | None = None
    day_id: UUID | None = None
    product_id: UUID | None = None
    weight_in_grams: float | None = None
    type: UserProductType = field(kw_only=True, default=UserProductType.LUNCH)
    calories: float | None = None
    proteins: float | None = None
    fats: float | None = None
    carbohydrates: float | None = None

    @classmethod
    def create(
            cls,
            product: Product,
            day: DailyUserConsumption,
            weight_in_grams: float | None = None,
            type: UserProductType = UserProductType.LUNCH,
    ) -> 'DailyUserProduct':
        entity = cls(
            id=cls.create_id(),
            updated_at=cls.create_now_time(),
            created_at=cls.create_now_time(),
            product=product,
            product_id=product.id,
            day=day,
            day_id=day.id,
            weight_in_grams=weight_in_grams,
            type=type,
        )
        entity.set_makros()
        day.add_product(entity)
        entity.clear_related_entities()
        return entity

    def set_makros(self) -> None:
        """
        Method to set makros for based on product.

        Returns: None

        """
        macro: MacroCalculatorStrategy = MacroCalculatorFactory.create_strategy(
            strategy_type=MacroCalculatorType.WEIGHT_STRATEGY
        )
        macro.calculate(self, self.product)

    def clear_related_entities(self) -> None:
        """
        Method to clear related entities.

        Method is used to clear related entities in `create` to:
            * avoid model imports etc.
            * it's easier to save entity to db with relations as `ID` only

        Returns: None

        """
        self.product = None
        self.day = None
