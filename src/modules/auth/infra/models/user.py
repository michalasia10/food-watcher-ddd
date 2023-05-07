import uuid

from sqlalchemy import Column, Text, Boolean, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType

from src.foundation.infrastructure.db import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())

    username = Column(Text(), nullable=False)
    password = Column(Text(), nullable=False)
    email = Column(EmailType(), nullable=False)
    first_name = Column(Text(), nullable=True)
    last_name = Column(Text(), nullable=True)
    is_active = Column(Boolean(), default=False)
    is_superuser = Column(Boolean(), default=False)
    daily_user_consumptions = relationship('DailyUserConsumption', back_populates='user')
    settings = relationship('UserSettings', back_populates='user')


class UserSettings(Base):
    __tablename__ = 'user_settings'
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), primary_key=True)
    user = relationship('User', back_populates='settings')
    daily_calories = Column(Float(), nullable=True)
    daily_proteins = Column(Float(), nullable=True)
    daily_fats = Column(Float(), nullable=True)
    daily_carbohydrates = Column(Float(), nullable=True)
