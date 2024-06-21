from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from src.foundation.infra.db import Base

product_recipe_association = Table(
    "product_recipe_association",
    Base.metadata,
    Column("product_id", UUID(as_uuid=True), ForeignKey("products.id")),
    Column("recipe_id", UUID(as_uuid=True), ForeignKey("recipes.id")),
)
