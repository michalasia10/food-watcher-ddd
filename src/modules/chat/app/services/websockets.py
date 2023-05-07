from abc import ABC, abstractmethod

from starlette.websockets import WebSocket

from modules.chat.domain.value_objects import ChanelId


class ConnectionManager(ABC):

    @abstractmethod
    async def connect(self, websocket: WebSocket, channel_id: ChanelId):
        ...

    @abstractmethod
    def disconnect(self, websocket: WebSocket, channel_id: ChanelId):
        ...

    @abstractmethod
    async def send_msg(self, channel_id: ChanelId, data: dict):
        ...
