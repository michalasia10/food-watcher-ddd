from abc import ABC, abstractmethod
from typing import NoReturn

from pydantic import BaseModel

from foundation.domain.entities import Entity
from foundation.domain.value_objects import UUID


class Command(BaseModel):
    pass


class CommandBase(ABC):

    @abstractmethod
    def create(self, entity: [Entity]) -> NoReturn:
        ...

    @abstractmethod
    def delete(self, id: [UUID]):
        ...

    def update(self, id: [UUID], entity: [Entity]):
        pass
