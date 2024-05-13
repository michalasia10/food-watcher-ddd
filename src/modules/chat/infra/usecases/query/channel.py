from src.foundation.domain.value_objects import UUID
from src.modules.chat.app.dtos import ChannelOutputDto, Message
from src.modules.chat.app.repository.messages import ChanelRepository
from src.modules.chat.app.usecases.query.channel import ChannelQuery as ChannelQueryBase
from src.modules.chat.domain.value_objects import ChanelId


class ChannelQuery(ChannelQueryBase):
    def __init__(self, repository: ChanelRepository):
        self._repository = repository

    def get_all(self, skip: int, limit: int) -> list[ChannelOutputDto]:
        return [
            ChannelOutputDto(
                id=ChanelId(channel.id),
                name=channel.name,
                messages=[
                    Message(
                        message=message.message,
                        channel_id=ChanelId(channel.id),
                        user_id=message.user_id,
                    )
                    for message in channel.messages
                ],
                participants_id=channel.participants_id,
            )
            for channel in self._repository.get_all_pagination(skip, limit)
        ]

    def get_by_id(self, id: UUID) -> ChannelOutputDto:
        chanel = self._repository.get_by_id(ChanelId(id))
        return ChannelOutputDto(**chanel.to_dict())
