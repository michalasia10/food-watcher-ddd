from abc import abstractmethod

from foundation.application.commands import CommandBase
from src.modules.chat.app.dtos import ChannelInputDto, ChannelOutputDto
from src.modules.chat.domain.value_objects import ChanelId


class ChannelCommand(CommandBase):

    @abstractmethod
    def create(self, chanel: ChannelInputDto) -> ChannelOutputDto:
        ...

    @abstractmethod
    def delete(self, id: ChanelId):
        ...

    @abstractmethod
    def update(self, id: ChanelId, chanel: ChannelInputDto) -> ChannelOutputDto:
        ...
