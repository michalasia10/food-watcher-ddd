from abc import ABC, abstractmethod

from pydantic import BaseModel

from src.foundation.domain.value_objects import UUID


class Query(BaseModel):
    pass


class QueryBase(ABC):

    @abstractmethod
    def get_all(self, skip: int, limit: int) -> list[BaseModel]: ...

    @abstractmethod
    def get_by_id(self, id: UUID) -> BaseModel:
        pass
