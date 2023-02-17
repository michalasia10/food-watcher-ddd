import uuid

from sqlalchemy import BigInteger, Column, Text, Float
from sqlalchemy.dialects.postgresql import UUID

from src.foundation.infrastructure.db import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    code = Column(BigInteger(), nullable=False)
    name = Column(Text(), nullable=False)
    quantity = Column(Text(), nullable=True)
    brand = Column(Text(), nullable=True)
    size = Column(Text(), nullable=True)
    groups = Column(Text(), nullable=True)
    category = Column(Text(), nullable=True)
    energy_kcal_100g = Column(Float(), nullable=False)
    fat_100g = Column(Float(), nullable=True)
    carbohydrates_100g = Column(Float(), nullable=True)
    sugars_100g = Column(Float(), nullable=True)
    proteins_100g = Column(Float(), nullable=True)
