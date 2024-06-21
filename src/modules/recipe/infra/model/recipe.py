from tortoise import fields

from src.core.infra.model import BaseModel


class Recipe(BaseModel):
    name = fields.CharField(null=False, max_length=255)
    link = fields.CharField(null=True, max_length=255)
    description = fields.TextField(null=True)
    summary_calories = fields.FloatField(null=True)
    summary_proteins = fields.FloatField(null=True)
    summary_fats = fields.FloatField(null=True)
    summary_carbohydrates = fields.FloatField(null=True)

    # relationships
    user = fields.ForeignKeyField("auth.User", related_name="recipes")
    products = fields.ReverseRelation["recipe.ProductForRecipe"]

    class Meta:
        app = "recipe"
        table = "recipe"
