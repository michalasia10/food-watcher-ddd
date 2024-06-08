from tortoise import fields
from uuid6 import uuid6

from src.core_new.infra.model import BaseModel


class ProductForRecipe(BaseModel):
    weight_in_grams = fields.FloatField(null=False)
    proteins = fields.FloatField(null=False)
    fats = fields.FloatField(null=False)
    carbohydrates = fields.FloatField(null=False)
    calories = fields.FloatField(null=False)

    # relationships
    product = fields.ForeignKeyField(
        'product.Product',
        related_name='recipe_for_product',
        to_field='id',
        default=uuid6,
        db_constraint=True,
    )
    recipe = fields.ForeignKeyField(
        'recipe.Recipe',
        related_name='products_for_recipe',
        to_field='id',
        default=uuid6,
        db_constraint=True,
    )

    class Meta:
        app = 'recipe'
        table = 'product_for_recipe'
