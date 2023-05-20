import uuid

from sqlalchemy import Column, Text, ForeignKey, ARRAY, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.foundation.infra.db import Base


class Channel(Base):
    __tablename__ = 'channel'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    participants_id = Column(ARRAY(UUID(as_uuid=True)), nullable=False)
    messages = relationship('Message', back_populates='channel')
    created_at = Column(DateTime(), default=func.now())
    name = Column(Text(), nullable=False)


class Message(Base):
    __tablename__ = 'message'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    message = Column(Text(), nullable=False)
    raw_bytes = Column(Text(), nullable=True)
    created_at = Column(DateTime(), default=func.now())

    # relationships
    channel_id = Column(UUID(as_uuid=True), ForeignKey('channel.id'))
    channel = relationship('Channel', back_populates='messages')
    user = relationship('User', back_populates='messages')
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'))
