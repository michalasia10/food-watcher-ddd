from tortoise import fields
from uuid6 import uuid6

from src.core.infra.model import BaseModel
from src.modules.product.domain.enum import UserProductType


class DailyUserProduct(BaseModel):
    weight_in_grams = fields.FloatField(null=False)
    type = fields.CharEnumField(
        enum_type=UserProductType, default=UserProductType.LUNCH.value
    )
    proteins = fields.FloatField(null=False)
    fats = fields.FloatField(null=False)
    carbohydrates = fields.FloatField(null=False)
    calories = fields.FloatField(null=False)

    # relationships
    day = fields.ForeignKeyField(
        "product.DailyUserConsumption",
        related_name="products",
        to_field="id",
        default=uuid6,
        db_constraint=True,
    )
    product = fields.ForeignKeyField(
        "product.Product",
        related_name="daily_user_products",
        to_field="id",
        default=uuid6,
        db_constraint=True,
    )

    class Meta:
        app = "product"
        table = "daily_user_product"
