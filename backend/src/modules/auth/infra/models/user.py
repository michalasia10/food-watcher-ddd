import uuid

from sqlalchemy import Column, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
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
