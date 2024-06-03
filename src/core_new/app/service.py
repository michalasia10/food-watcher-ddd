from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from src.core_new.domain.entity import Entity
from src.core_new.domain.repo import IRepository


class ICrudService(ABC):

    @abstractmethod
    async def create(self, input_dto: BaseModel): ...

    @abstractmethod
    async def get_all(self, skip: int, limit: int): ...

    @abstractmethod
    async def get_by_id(self, id: UUID): ...

    @abstractmethod
    async def update(self, id: UUID, input_dto: BaseModel, user_id: Optional[UUID] = None, is_admin: bool = False): ...

    @abstractmethod
    async def delete(self, id: UUID, user_id: Optional[UUID] = None, is_admin: bool = False): ...


class BaseCrudService(ICrudService):
    OUTPUT_DTO: BaseModel = None
    NOT_RECORD_OWNER_ERROR = None
    NOT_FOUND_ERROR = None
    DOES_NOT_EXIST_ERROR = None

    def __init__(self, repository: [IRepository]):
        self._repository = repository

    @abstractmethod
    async def create(self, input_dto):
        ...

    async def update(self, id: UUID, input_dto: BaseModel, user_id: UUID = None, is_admin=False) -> BaseModel:
        if not is_admin and (user_id and user_id != id):
            raise self.NOT_RECORD_OWNER_ERROR

        entity: Entity = await self._repository.aget_by_id(id)
        entity.update(input_dto)

        await self._repository.aupdate(entity)
        fresh_entity: Entity = await self._repository.aget_by_id(id)

        return self.OUTPUT_DTO(**fresh_entity.snapshot)

    async def delete(self, id: UUID, user_id: UUID = None, is_admin=False) -> None:
        if not is_admin and (user_id and user_id != id):
            raise self.NOT_RECORD_OWNER_ERROR

        entity: Entity = await self.get_by_id(id)
        await self._repository.adelete(entity)

    async def get_all(self, skip: int, limit: int) -> list[BaseModel]:
        entities: list[Entity] = await self._repository.aget_all(offset=skip, limit=limit)

        return [self.OUTPUT_DTO(**entity.snapshot) for entity in entities]

    async def get_by_id(self, id: UUID) -> BaseModel:
        try:
            entity: Entity = await self._repository.aget_by_id(id)
        except  self.DOES_NOT_EXIST_ERROR:
            raise self.NOT_FOUND_ERROR

        return self.OUTPUT_DTO(**entity.snapshot)


class IAuthService(ABC):

    @abstractmethod
    async def authenticate(self, credentials: str): ...

    @abstractmethod
    async def verify(self, token: str): ...
