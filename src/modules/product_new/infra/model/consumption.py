from tortoise import fields
from uuid6 import uuid6

from src.core_new.infra.model import BaseModel


class DailyUserConsumption(BaseModel):
    date = fields.DateField(null=False)
    summary_calories = fields.FloatField(null=False)
    summary_proteins = fields.FloatField(null=False)
    summary_fats = fields.FloatField(null=False)
    summary_carbohydrates = fields.FloatField(null=False)

    # relationships
    user = fields.ForeignKeyField(
        'auth.User',
        related_name='daily_user_consumptions',
        to_field='id',
        default=uuid6,
        db_constraint=True,
    )


    class Meta:
        app = 'product'
        table = 'daily_user_consumption'
