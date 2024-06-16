# import json
# from asyncio import AbstractEventLoop
# from typing import AsyncIterator, NoReturn
#
# from aio_pika import Message, ExchangeType, connect_robust
# from aio_pika.abc import (
#     AbstractChannel,
#     AbstractQueue,
#     AbstractExchange,
#     AbstractRobustConnection,
# )
#
# from modules.chat.domain.value_objects import ChanelId
# from src.modules.chat.app.dtos import Message as MessageDto
# from src.modules.chat.app.services.notifications import AioPikaClientBase
#
#
# class AioPikaClient(AioPikaClientBase):
#     def __init__(
#         self, channel_id: ChanelId, loop: AbstractEventLoop, rabitmq_url: str
#     ) -> None:
#         self._loop = loop
#         self._channel_id = channel_id
#         self._rabitmq_url = rabitmq_url
#
#     async def _init(self) -> None:
#         self._connection: [AbstractRobustConnection] = await connect_robust(
#             self._rabitmq_url, loop=self._loop
#         )
#
#         self._channel: AbstractChannel = await self._connection.channel()
#         self._exchange: [AbstractExchange] = await self._channel.declare_exchange(
#             "notifications", ExchangeType.FANOUT
#         )
#         self._routing_key = "notify-x"
#         self._queue: [AbstractQueue] = await self._channel.declare_queue(
#             str(self._channel_id), auto_delete=True
#         )
#         await self._queue.bind(exchange=self._exchange, routing_key=self._routing_key)
#
#     async def config(self):
#         await self._init()
#
#     async def close(self) -> NoReturn:
#         """Close the connection."""
#         await self._connection.close()
#
#     async def publish_message(self, message: MessageDto) -> None:
#         """
#         Send a notification to the specified channel
#         """
#         await self._exchange.publish(
#             Message(body=json.dumps(message).encode()), routing_key=self._routing_key
#         )
#
#     async def receive_notifications(self) -> AsyncIterator[dict]:
#         """
#         Receive messages from the specified channel
#         """
#         async with self._queue.iterator() as queue_iter:
#             async for message in queue_iter:
#                 async with message.process():
#                     yield json.loads(message.body)
