from enum import Enum

from src.modules.common.macro.strategies import (
    MacroCalculatorStrategy,
    MacroCalculatorWeightStrategy,
    MacroCalculatorSummaryStrategy,
    MacroCalculatorSubtractStrategy
)


class MacroCalculatorType(int, Enum):
    SUMMARY_STRATEGY = 1
    WEIGHT_STRATEGY = 2
    SUBTRACT_STRATEGY = 3


class MacroCalculatorFactory:
    @classmethod
    def create_strategy(cls, strategy_type: int) -> [MacroCalculatorStrategy]:
        match strategy_type:
            case MacroCalculatorType.WEIGHT_STRATEGY.value:
                return MacroCalculatorWeightStrategy
            case MacroCalculatorType.SUMMARY_STRATEGY.value:
                return MacroCalculatorSummaryStrategy
            case MacroCalculatorType.SUBTRACT_STRATEGY.value:
                return MacroCalculatorSubtractStrategy
            case _:
                raise ValueError(f"Unknown strategy type: {strategy_type}")
