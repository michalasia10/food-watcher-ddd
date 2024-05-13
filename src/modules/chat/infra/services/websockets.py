from starlette.websockets import WebSocket

from src.modules.chat.app.services.websockets import (
    ConnectionManager as ConnectionManagerBase,
)


class ConnectionManager(ConnectionManagerBase):
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def subscribe(self, channel_id: str, websocket: WebSocket):
        self.active_connections.setdefault(channel_id, []).append(websocket)

    def unsubscribe(self, channel_id: str, websocket: WebSocket):
        self.active_connections.get(channel_id, []).remove(websocket)

    async def connect(self, websocket: WebSocket, channel_id: str):
        await websocket.accept()
        await self.subscribe(channel_id, websocket)

    def disconnect(self, websocket: WebSocket, channel_id: str):
        self.unsubscribe(channel_id, websocket)
        if not self.active_connections.get(channel_id):
            del self.active_connections[channel_id]

    async def send_msg(self, channel_id: str, data: dict):
        for connection in self.active_connections.get(channel_id, []):
            await connection.send_json(data)

    def get_channel_connections(self, channel_id: str):
        return self.active_connections.get(channel_id, [])
