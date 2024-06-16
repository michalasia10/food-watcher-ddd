from tortoise import fields

from src.core_new.infra.model import BaseModel


class Product(BaseModel):
    code = fields.BigIntField(null=False)
    name = fields.CharField(null=False, max_length=255)
    quantity = fields.CharField(null=True, max_length=255)
    brand = fields.CharField(null=True, max_length=255)
    size = fields.CharField(null=True, max_length=255)
    groups = fields.CharField(null=True, max_length=255)
    category = fields.CharField(null=True, max_length=255)
    energy_kcal_100g = fields.FloatField(null=False)
    fat_100g = fields.FloatField(null=True)
    carbohydrates_100g = fields.FloatField(null=True)
    sugars_100g = fields.FloatField(null=True)
    proteins_100g = fields.FloatField(null=True)

    # relationships
    user = fields.ForeignKeyField('auth.User', related_name='products', null=True)
    daily_user_products = fields.ReverseRelation['ToDo']
    product_for_recipes = fields.ReverseRelation['ToDo']

    class Meta:
        app = 'product'
        table = 'product'
