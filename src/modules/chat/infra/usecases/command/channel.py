import dataclasses

from modules.chat.domain.exceptions import ChannelAlreadyExists, ChannelNotFound
from src.modules.chat.app.dtos import ChannelInputDto, ChannelOutputDto
from src.modules.chat.app.repository.messages import ChanelRepository
from src.modules.chat.app.usecases.command.channel import ChannelCommand as ChannelCommandBase
from src.modules.chat.domain.entities import Channel
from src.modules.chat.domain.value_objects import ChanelId


class ChannelCommand(ChannelCommandBase):
    def __init__(self, repository: ChanelRepository):
        self._repository = repository

    def create(self, chanel: ChannelInputDto) -> ChannelOutputDto:
        if self._repository.exists('name', chanel.name):
            raise ChannelAlreadyExists('Channel already exists.')


        channel = self._repository.create(Channel(**dataclasses.asdict(chanel)))
        return ChannelOutputDto(id=channel.id, name=channel.name)

    def delete(self, id: ChanelId):
        if not self._repository.exists('id', id):
            raise ChannelNotFound('Chanel not found.')

        self._repository.delete(id)

    def update(self, id: ChanelId, chanel: ChannelInputDto) -> ChannelOutputDto:
        return self._repository.update(Channel(**dataclasses.asdict(chanel)))
