from abc import ABC, abstractmethod


class MacroCalculatorStrategy(ABC):
    @classmethod
    @abstractmethod
    def calculate(cls, object_to_set, product): ...


class MacroCalculatorWeightStrategy(MacroCalculatorStrategy):
    @classmethod
    def calculate_calories(cls, object_to_set, product):
        assert hasattr(
            object_to_set, "weight_in_grams"
        ), "Object must have weight_in_grams attribute"
        assert hasattr(object_to_set, "calories"), "Object must have calories attribute"

        object_to_set.calories = (
            object_to_set.weight_in_grams * product.energy_kcal_100g / 100
            if product.energy_kcal_100g
            else 0
        )

    @classmethod
    def calculate_proteins(cls, object_to_set, product=None):
        assert hasattr(
            object_to_set, "weight_in_grams"
        ), "Object must have weight_in_grams attribute"
        assert hasattr(object_to_set, "proteins"), "Object must have proteins attribute"

        object_to_set.proteins = (
            object_to_set.weight_in_grams * product.proteins_100g / 100
            if product.proteins_100g
            else 0
        )

    @classmethod
    def calculate_fats(cls, object_to_set, product=None):
        assert hasattr(
            object_to_set, "weight_in_grams"
        ), "Object must have weight_in_grams attribute"
        assert hasattr(object_to_set, "fats"), "Object must have fats attribute"

        object_to_set.fats = (
            object_to_set.weight_in_grams * product.fat_100g / 100
            if product.fat_100g
            else 0
        )

    @classmethod
    def calculate_carbohydrates(cls, object_to_set, product=None):
        assert hasattr(
            object_to_set, "weight_in_grams"
        ), "Object must have weight_in_grams attribute"
        assert hasattr(
            object_to_set, "carbohydrates"
        ), "Object must have carbohydrates attribute"

        object_to_set.carbohydrates = (
            object_to_set.weight_in_grams * product.carbohydrates_100g / 100
            if product.carbohydrates_100g
            else 0
        )

    @classmethod
    def calculate(cls, object_to_set, product):
        for method in [
            "calculate_calories",
            "calculate_proteins",
            "calculate_fats",
            "calculate_carbohydrates",
        ]:
            getattr(cls, method)(object_to_set, product)


class MacroCalculatorSummaryStrategy(MacroCalculatorStrategy):
    @classmethod
    def calculate(cls, object_to_set, product):
        for attr in [
            "summary_calories",
            "summary_proteins",
            "summary_fats",
            "summary_carbohydrates",
        ]:
            assert hasattr(object_to_set, attr), "Object must have {} attribute".format(
                attr
            )

        object_to_set.summary_calories += product.calories
        object_to_set.summary_proteins += product.proteins
        object_to_set.summary_fats += product.fats
        object_to_set.summary_carbohydrates += product.carbohydrates


class MacroCalculatorSubtractStrategy(MacroCalculatorStrategy):
    @classmethod
    def calculate(cls, object_to_set, product):
        for attr in [
            "summary_calories",
            "summary_proteins",
            "summary_fats",
            "summary_carbohydrates",
        ]:
            assert hasattr(object_to_set, attr), "Object must have {} attribute".format(
                attr
            )

        object_to_set.summary_calories -= product.calories
        object_to_set.summary_proteins -= product.proteins
        object_to_set.summary_fats -= product.fats
        object_to_set.summary_carbohydrates -= product.carbohydrates
