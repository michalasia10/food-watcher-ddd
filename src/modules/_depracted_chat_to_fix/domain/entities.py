# from dataclasses import field
#
# from pydantic.dataclasses import dataclass
#
# from foundation.domain.value_objects import UUID
# from src.foundation.domain.entities import AggregateRoot
#
#
# @dataclass(kw_only=True)
# class Message(AggregateRoot):
#     message: str = ""
#     user_id: UUID = ""
#     channel_id: UUID = ""
#
#
# @dataclass(kw_only=True)
# class Channel(AggregateRoot):
#     name: str = ""
#     participants_id: list[UUID] = field(default_factory=list)
#     messages: list[Message] = field(default_factory=list)
