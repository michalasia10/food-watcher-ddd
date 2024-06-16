# import dataclasses
# import json
# from asyncio import AbstractEventLoop
# from typing import final
#
# from starlette.websockets import WebSocket, WebSocketState
#
# from foundation.infra.logging import logger
# from modules.chat.app.dtos import Message as MessageDto, WebSockMessage
# from src.modules.chat.app.repository.messages import MessageCompositeRepository
# from src.modules.chat.app.services.websockets import ConnectionManager
# from src.modules.chat.domain.entities import Message
# from src.modules.chat.domain.value_objects import ChanelId
# from src.modules.chat.infra.services.notifications import AioPikaClient
#
#
# @final
# class WebSocketFacade:
#     def __init__(
#         self,
#         ws: WebSocket,
#         channel_id: ChanelId,
#         connection_manager: ConnectionManager,
#         loop: AbstractEventLoop,
#         rabitmq_url: str,
#         message_repository: MessageCompositeRepository,
#     ):
#         self._message_repository = message_repository
#         self._ws = ws
#         self._channel_id = channel_id
#         self._con_manager = connection_manager
#         self._loop = loop
#         self._rabbitmq_url = rabitmq_url
#
#     async def _connect(self, channel_id: ChanelId):
#         await self._con_manager.connect(self._ws, channel_id)
#         await self._load_previous_messages(channel_id)
#
#     async def _send_message(self, message: dict):
#         logger.info(
#             f"Message received for channel {self._channel_id}. Message: {json.dumps(message)}"
#         )
#         await self._con_manager.send_msg(self._channel_id, message)
#
#     async def _load_previous_messages(self, channel_id: ChanelId):
#         messages: list[Message] = self._message_repository.load_previous_messages(
#             channel_id
#         )
#         for message in messages:
#             await self._send_message(message.to_serializer_dict())
#
#     async def run(self):
#         pika = AioPikaClient(self._channel_id, self._loop, self._rabbitmq_url)
#         await pika.config()
#
#         try:
#             await self._connect(self._channel_id)
#             while True:
#                 async for message in pika.receive_notifications():
#                     if message:
#                         logger.info(
#                             f"Message send for channel {self._channel_id}. Message: {message}"
#                         )
#                         await self._send_message(message)
#
#                 if self._ws.client_state == WebSocketState.DISCONNECTED:
#                     logger.info(
#                         "Connection will be disconnected. ",
#                         extra={"data": "Client disconnected"},
#                     )
#                     break
#
#         except Exception as e:
#             logger.info(
#                 f"Connection will be disconnected cause: {e}", extra={"data": e}
#             )
#             self._con_manager.disconnect(self._ws, self._channel_id)
#             await self._con_manager.send_msg(
#                 self._channel_id, {"message": "Someone disconnected."}
#             )
#             await pika.close()
#
#
# @final
# class NotificationPublisherFacade:
#     def __init__(
#         self,
#         channel_id: ChanelId,
#         message: WebSockMessage,
#         rabitmq_url: str,
#         message_repository: MessageCompositeRepository,
#         loop: AbstractEventLoop,
#         user,
#     ):
#         self._channel_id = channel_id
#         self._message = message
#         self._user = user
#         self._loop = loop
#         self._rabitmq_url = rabitmq_url
#         self._message_repository = message_repository
#
#     def _channel_not_exists(self):
#         return not self._message_repository.channel_exists(ChanelId(self._channel_id))
#
#     async def publish(self):
#         pika_client = AioPikaClient(self._channel_id, self._loop, self._rabitmq_url)
#         await pika_client.config()
#
#         if self._channel_not_exists():
#             raise Exception(f"Channel {self._channel_id} doesn't exists.")
#
#         try:
#             message = MessageDto(
#                 user_id=self._user.id,
#                 channel_id=self._channel_id,
#                 **self._message.dict(),
#             )
#             await pika_client.publish_message(message.dict())
#             self._message_repository.create(Message(**dataclasses.asdict(message)))
#
#         except Exception as e:
#             logger.info(
#                 f"Connection will be disconnected cause: {e}", extra={"data": e}
#             )
#             await pika_client.close()
#             raise e
