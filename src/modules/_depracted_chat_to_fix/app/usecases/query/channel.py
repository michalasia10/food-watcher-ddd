# from abc import abstractmethod
#
# from modules.chat.app.dtos import ChannelOutputDto
# from src.foundation.application.queries import QueryBase
# from src.foundation.domain.value_objects import UUID
#
#
# class ChannelQuery(QueryBase):
#
#     @abstractmethod
#     def get_all(self, skip: int, limit: int) -> list[ChannelOutputDto]: ...
#
#     @abstractmethod
#     def get_by_id(self, id: UUID) -> ChannelOutputDto: ...
