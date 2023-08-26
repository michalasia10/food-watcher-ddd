from abc import ABC
from abc import abstractmethod
from typing import Any, NoReturn

from src.foundation.domain.repository import GenericRepository
from src.modules.chat.domain.entities import Message, Channel
from src.modules.chat.domain.value_objects import ChanelId


class ChanelRepository(GenericRepository):

    @abstractmethod
    def get_by_id(self, id: ChanelId):
        ...

    @abstractmethod
    def get_by_field_value(self, field: str, value: Any):
        ...

    @abstractmethod
    def update(self, entity: Channel) -> NoReturn:
        ...

    @abstractmethod
    def create(self, entity: Channel) -> NoReturn:
        ...

    @abstractmethod
    def get_all(self) -> list[Channel]:
        ...

    @abstractmethod
    def get_all_pagination(self, skip: int, limit: int) -> list[Channel]:
        ...


class MessageRepository(ABC):

    @abstractmethod
    def get_all_by_channel(self, channel_id: ChanelId) -> list[Message]:
        ...

    @abstractmethod
    def create(self, entity: Message):
        ...


class MessageCompositeRepository(ABC):

    @abstractmethod
    def create(self, entity: Message):
        ...

    @abstractmethod
    def channel_exists(self, chanel_id: ChanelId) -> bool:
        ...

    @abstractmethod
    def load_previous_messages(self, channel_id: ChanelId) -> list[Message]:
        ...