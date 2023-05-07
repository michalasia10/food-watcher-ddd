from dataclasses import dataclass, asdict

from pydantic.typing import Optional

from foundation.domain.value_objects import UUID
from src.modules.chat.domain.value_objects import ChanelId


@dataclass(frozen=True)
class MessageBase:
    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}


@dataclass(frozen=True)
class ChannelInputDto(MessageBase):
    name: str
    participants_id: list[UUID] = None


@dataclass(frozen=True)
class WebSockMessage(MessageBase):
    message: str
    raw_bytes: Optional[bytes] = None


@dataclass(frozen=True)
class Message(MessageBase):
    message: str
    channel_id: ChanelId
    user_id: UUID
    raw_bytes: bytes | None = None


@dataclass(frozen=True)
class ChannelOutputDto:
    id: ChanelId
    name: str
    messages: list[Message] = None
    participants_id: list[UUID] = None
