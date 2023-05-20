import uuid

from sqlalchemy import BigInteger, Column, Text, Float, ForeignKey, DateTime, func, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from src.foundation.infra.db import Base
from src.foundation.infra.db import LabeledEnum


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
    daily_user_products = relationship('DailyUserProducts', back_populates='product')


class UserProductType(LabeledEnum):
    regular = 1
    ingredient = 2


class DailyUserConsumption(Base):
    __tablename__ = 'daily_user_consumption'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'))
    user = relationship('User', back_populates='daily_user_consumptions')
    products = relationship('DailyUserProducts', back_populates='day')
    time_updated = Column(DateTime(), onupdate=func.now())
    date = Column(DateTime(), default=func.now())
    summary_calories = Column(Float(), nullable=True)
    summary_proteins = Column(Float(), nullable=True)
    summary_fats = Column(Float(), nullable=True)
    summary_carbohydrates = Column(Float(), nullable=True)

    class Meta:
        children = ['products']


class DailyUserProducts(Base):
    __tablename__ = 'daily_user_products'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    day_id = Column(UUID(as_uuid=True), ForeignKey('daily_user_consumption.id'))
    day = relationship('DailyUserConsumption', back_populates='products')
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'))
    product = relationship('Product', back_populates='daily_user_products')
    weight_in_grams = Column(Float(), nullable=False)
    type = Column(ChoiceType(choices=UserProductType, impl=Integer()), default=UserProductType.regular)
    time_updated = Column(DateTime(), onupdate=func.now())
    calories = Column(Float(), nullable=True)
    proteins = Column(Float(), nullable=True)
    fats = Column(Float(), nullable=True)
    carbohydrates = Column(Float(), nullable=True)

    class Meta:
        children = ['product']
