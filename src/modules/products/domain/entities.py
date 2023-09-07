from datetime import datetime
from typing import Any

from pydantic import Field
from pydantic.dataclasses import dataclass

from foundation.domain.value_objects import UUID
from src.foundation.domain.entities import AggregateRoot
from src.modules.products.infra.models.product import (
    Product as ProductModel,
    DailyUserProducts as DailyUserProductModel,
    DailyUserConsumption as DailyUserConsumptionModel, UserProductType
)


@dataclass
class RecipeProduct(AggregateRoot):
    name: str | None = None
    link: str | None = None
    description: str | None = None


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
    recipes: list[RecipeProduct] = Field(default_factory=list)

    class Meta:
        orm_model = ProductModel


@dataclass
class DailyUserProduct(AggregateRoot):
    day_id: UUID | None = None
    weight_in_grams: float | None = None
    type: UserProductType | None | int = None
    product_id: UUID | None = None
    product: Product | Any | None = None
    calories: float | None = None
    proteins: float | None = None
    fats: float | None = None
    carbohydrates: float | None = None

    class Meta:
        orm_model = DailyUserProductModel

    def calculate_calories(self, product=None):
        _product = product or self.product
        self.calories = self.weight_in_grams * _product.energy_kcal_100g / 100 if _product.energy_kcal_100g else 0

    def calculate_proteins(self, product=None):
        _product = product or self.product
        self.proteins = self.weight_in_grams * _product.proteins_100g / 100 if _product.proteins_100g else 0

    def calculate_fats(self, product=None):
        _product = product or self.product
        self.fats = self.weight_in_grams * _product.fat_100g / 100 if _product.fat_100g else 0

    def calculate_carbohydrates(self, product=None):
        _product = product or self.product
        self.carbohydrates = self.weight_in_grams * _product.carbohydrates_100g / 100 if _product.carbohydrates_100g else 0

    def calculate_macros(self, product=None):
        self.calculate_calories(product)
        self.calculate_proteins(product)
        self.calculate_fats(product)
        self.calculate_carbohydrates(product)


@dataclass
class DailyUserConsumption(AggregateRoot):
    user_id: UUID | None = None
    date: datetime | None = None
    products: list[DailyUserProduct | None] = Field(default_factory=list)
    summary_calories: float | None = 0
    summary_proteins: float | None = 0
    summary_fats: float | None = 0
    summary_carbohydrates: float | None = 0

    class Meta:
        orm_model = DailyUserConsumptionModel

    def create_date(self, date=None):
        self.date = date or datetime.now()

    def add_product(self, product: DailyUserProduct):
        self.create_date()
        self.summary_calories += product.calories
        self.summary_proteins += product.proteins
        self.summary_fats += product.fats
        self.summary_carbohydrates += product.carbohydrates

    def delete_product(self, product: DailyUserProduct):
        self.products.remove(product)
        self.summary_calories -= product.calories
        self.summary_proteins -= product.proteins
        self.summary_fats -= product.fats
        self.summary_carbohydrates -= product.carbohydrates
