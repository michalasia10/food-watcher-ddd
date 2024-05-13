from typing import Any, final

from src.foundation.infra.repository import Repository
from src.modules.chat.app.repository.messages import (
    ChanelRepository as ChannelRepositoryBase,
    MessageRepository as MessageRepositoryBase,
    MessageCompositeRepository as MessageCompositeRepositoryBase,
)
from src.modules.chat.domain.entities import Channel as ChannelE, Message as MessageE
from src.modules.chat.domain.value_objects import ChanelId
from src.modules.chat.infra.models.messages import Message, Channel


@final
class SqlChannelRepository():
    pass
    # model = Channel
    #
    # def get_by_id(self, id: ChanelId) -> ChannelE:
    #     return self.get_by_field_value("id", id)
    #
    # def get_by_field_value(self, field: str, value: Any) -> ChannelE:
    #     data = self.session.query(self.model).filter_by(**{field: value}).first()
    #     return self.data_to_entity(data, ChannelE)
    #
    # def update(self, entity: ChannelE) -> None:
    #     raise NotImplementedError
    #
    # def create(self, entity: ChannelE) -> ChannelE:
    #     self.session.add(self.entity_to_model(entity))
    #     return entity
    #
    # def get_all(self) -> list[ChannelE]:
    #     data = self.session.query(self.model).all()
    #     return [self.data_to_entity(dat, ChannelE) for dat in data]
    #
    # def get_all_pagination(self, skip: int, limit: int) -> list[ChannelE]:
    #     data = self.session.query(self.model).offset(skip).limit(limit).all()
    #     return [self.data_to_entity(dat, ChannelE) for dat in data]
    #
    # def delete(self, id: ChanelId):
    #     raise NotImplementedError
    #
    # def exists(self, field: str, value: Any) -> bool:
    #     return bool(self.session.query(self.model).filter_by(**{field: value}).first())


@final
class SqlMessageRepository():
    pass

    # def create(self, entity: MessageE) -> MessageE:
    #     self.session.add(self.entity_to_model(entity))
    #     return entity
    #
    # def get_all_by_channel(self, channel_id: ChanelId) -> list[MessageE]:
    #     data = (
    #         self.session.query(self.model).filter_by(channel_id=str(channel_id)).all()
    #     )
    #     return [self.data_to_entity(dat, MessageE) for dat in data]


@final
class SqlMessageCompositeRepository():
    pass
    # def __init__(
    #     self,
    #     channel_repository: ChannelRepositoryBase,
    #     message_repository: MessageRepositoryBase,
    # ):
    #     self._channel_repository = channel_repository
    #     self._message_repository = message_repository
    #
    # def create(self, entity: Message):
    #     self._message_repository.create(entity)
    #
    # def channel_exists(self, chanel_id: ChanelId) -> bool:
    #     return self._channel_repository.exists("id", chanel_id)
    #
    # def load_previous_messages(self, channel_id: ChanelId) -> list[Message]:
    #     return self._message_repository.get_all_by_channel(channel_id)
