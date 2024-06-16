# from abc import ABC, abstractmethod
# from asyncio import AbstractEventLoop
#
# from typing import Iterator
#
#
# class AioPikaClientBase(ABC):
#
#     @abstractmethod
#     def __init__(self, channel_id: int, loop: AbstractEventLoop, rabitmq_url: str): ...
#
#     @abstractmethod
#     def close(self): ...
#
#     @abstractmethod
#     async def publish_message(self, message: dict): ...
#
#     @abstractmethod
#     async def receive_notifications(self) -> Iterator[str]: ...
