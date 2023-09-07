import uuid

from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.foundation.infra.db import Base
from src.modules.recipe_managment.product_recipe_association import product_recipe_association


class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    name = Column(Text(), nullable=False)
    link = Column(Text(), nullable=True)
    description = Column(Text(), nullable=True)
    products = relationship('Product', secondary=product_recipe_association, back_populates='recipes')

    class Meta:
        children = ['products']
