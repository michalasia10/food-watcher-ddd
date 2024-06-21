import uuid

from sqlalchemy import Column, Text, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.foundation.infra.db import Base


class ProductForRecipe(Base):
    __tablename__ = 'product_for_recipe'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    weight_in_grams = Column(Float(), nullable=False)
    calories = Column(Float(), nullable=True)
    proteins = Column(Float(), nullable=True)
    fats = Column(Float(), nullable=True)
    carbohydrates = Column(Float(), nullable=True)

    # relationships

    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'))
    product = relationship('Product', back_populates='product_for_recipes')

    recipe_id = Column(UUID(as_uuid=True), ForeignKey('recipes.id'))
    recipe = relationship('Recipe', back_populates='products')

    class Meta:
        children = ['product']


class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    name = Column(Text(), nullable=False)
    link = Column(Text(), nullable=True)
    description = Column(Text(), nullable=True)
    summary_calories = Column(Float(), nullable=True)
    summary_proteins = Column(Float(), nullable=True)
    summary_fats = Column(Float(), nullable=True)
    summary_carbohydrates = Column(Float(), nullable=True)

    # relationships
    products = relationship('ProductForRecipe', back_populates='recipe')

    class Meta:
        children = ['products']
