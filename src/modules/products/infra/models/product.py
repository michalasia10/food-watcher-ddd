# import uuid
#
# from sqlalchemy import (
#     BigInteger,
#     Column,
#     Text,
#     Float,
#     ForeignKey,
#     DateTime,
#     func,
#     Integer,
# )
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.orm import relationship
# from sqlalchemy_utils import ChoiceType
#
# from src.foundation.infra.db import Base
from src.foundation.infra.db import LabeledEnum
#
#
class Product():
    pass
#     __tablename__ = "products"
#
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
#     code = Column(BigInteger(), nullable=False)
#     name = Column(Text(), nullable=False)
#     quantity = Column(Text(), nullable=True)
#     brand = Column(Text(), nullable=True)
#     size = Column(Text(), nullable=True)
#     groups = Column(Text(), nullable=True)
#     category = Column(Text(), nullable=True)
#     energy_kcal_100g = Column(Float(), nullable=False)
#     fat_100g = Column(Float(), nullable=True)
#     carbohydrates_100g = Column(Float(), nullable=True)
#     sugars_100g = Column(Float(), nullable=True)
#     proteins_100g = Column(Float(), nullable=True)
#
#     # relationships
#     daily_user_products = relationship("DailyUserProducts", back_populates="product")
#     product_for_recipes = relationship("ProductForRecipe", back_populates="product")
#
#     class Meta:
#         children = ["product_for_recipes"]
#
#
class UserProductType(LabeledEnum):
    breakfast = 1
    lunch = 2
    dinner = 3

#
class DailyUserConsumption():
    pass
#     __tablename__ = "daily_user_consumption"
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
#     time_updated = Column(DateTime(), onupdate=func.now())
#     date = Column(DateTime())
#     summary_calories = Column(Float(), nullable=True)
#     summary_proteins = Column(Float(), nullable=True)
#     summary_fats = Column(Float(), nullable=True)
#     summary_carbohydrates = Column(Float(), nullable=True)
#
#     # relationships
#     user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
#     user = relationship("User", back_populates="daily_user_consumptions")
#     products = relationship("DailyUserProducts", back_populates="day")
#
#     class Meta:
#         children = ["products"]
#
#
class DailyUserProducts():
    pass
#     __tablename__ = "daily_user_products"
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
#     day_id = Column(UUID(as_uuid=True), ForeignKey("daily_user_consumption.id"))
#     day = relationship("DailyUserConsumption", back_populates="products")
#     product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))
#     product = relationship("Product", back_populates="daily_user_products")
#     weight_in_grams = Column(Float(), nullable=False)
#     type = Column(
#         ChoiceType(choices=UserProductType, impl=Integer()),
#         default=UserProductType.breakfast,
#     )
#     time_updated = Column(DateTime(), onupdate=func.now())
#     calories = Column(Float(), nullable=True)
#     proteins = Column(Float(), nullable=True)
#     fats = Column(Float(), nullable=True)
#     carbohydrates = Column(Float(), nullable=True)
#
#     class Meta:
#         children = ["product"]
