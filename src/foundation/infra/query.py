from typing import Generic, TypeVar
from uuid import UUID as UUDIBase

from src.foundation.application.queries import Query as QueryBase
from src.foundation.domain.repository import GenericRepository

OutPutDto = TypeVar("OutPutDto")
UUID = TypeVar("UUID", bound=UUDIBase)


class Query(QueryBase, Generic[OutPutDto]):
    output_dto: OutPutDto

    def __init__(self, repository: GenericRepository):
        self._repository = repository

    def get_all(self, skip: int = 0, limit: int = 100) -> list[OutPutDto]:
        self._repository.get_all()
        return [
            self.output_dto(**entity.to_dict())
            for entity in self._repository.get_all_pagination(skip, limit)
        ]

    def get_by_id(self, id: UUID) -> OutPutDto:
        entity = self._repository.get_by_id(id)
        return self.output_dto(**entity.to_dict())
