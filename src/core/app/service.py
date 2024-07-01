from abc import ABC, abstractmethod
from typing import Optional, Type
from uuid import UUID

from loguru import logger
from pydantic import BaseModel

from src.core.domain.entity import Entity
from src.core.domain.errors import Error
from src.core.domain.repo import IRepository


class ICrudService(ABC):
    @abstractmethod
    async def create(
        self, input_dto: BaseModel, user_id: UUID = None, is_admin: bool = False
    ): ...

    @abstractmethod
    async def get_all(self, skip: int, limit: int): ...

    @abstractmethod
    async def get_by_id(self, id: UUID): ...

    @abstractmethod
    async def update(
        self,
        id: UUID,
        input_dto: BaseModel,
        user_id: Optional[UUID] = None,
        is_admin: bool = False,
    ): ...

    @abstractmethod
    async def delete(
        self, id: UUID, user_id: Optional[UUID] = None, is_admin: bool = False
    ): ...


class BaseCrudService(ICrudService):
    OUTPUT_DTO: BaseModel = None
    NOT_RECORD_OWNER_ERROR = None
    NOT_FOUND_ERROR = None
    DOES_NOT_EXIST_ERROR = None

    def __init__(self, repository: [IRepository]):
        self._repository = repository

    @abstractmethod
    async def create(self, input_dto, user_id: UUID = None, is_admin: bool = False): ...

    @staticmethod
    def _raise(error: tuple[Type[Error], str], id: UUID = None):
        _exception, msg = error
        raise _exception(msg.format(id=id) if "id" in msg else msg)

    async def update(
        self, id: UUID, input_dto: BaseModel, user_id: UUID = None, is_admin=False
    ) -> BaseModel:
        entity: Entity = await self._repository.aget_by_id(id)

        if not is_admin and (
            (hasattr(entity, "user_id") and getattr(entity, "user_id") != user_id)
            or (hasattr(entity, "username") and getattr(entity, "id") != user_id)
        ):
            self._raise(self.NOT_RECORD_OWNER_ERROR, id=id)

        entity.update(input_dto)

        await self._repository.aupdate(entity)

        logger.info("Entity[{entity}] updated", entity=str(entity))
        fresh_entity: Entity = await self._repository.aget_by_id(id)

        return self.OUTPUT_DTO(**fresh_entity.snapshot)

    async def delete(self, id: UUID, user_id: UUID = None, is_admin=False) -> None:
        entity: Entity = await self._repository.aget_by_id(id)

        if not is_admin and (
            (hasattr(entity, "user_id") and getattr(entity, "user_id") != user_id)
            or (hasattr(entity, "username") and getattr(entity, "id") != user_id)
        ):
            self._raise(self.NOT_RECORD_OWNER_ERROR, id=id)

        await self._repository.adelete(entity)
        logger.info("Entity[{entity}] deleted", entity=str(entity))

    async def get_all(self, skip: int, limit: int) -> list[BaseModel]:
        entities: list[Entity] = await self._repository.aget_all(
            offset=skip, limit=limit
        )

        return [self.OUTPUT_DTO(**entity.snapshot) for entity in entities]

    async def get_by_id(self, id: UUID) -> BaseModel:
        try:
            entity: Entity = await self._repository.aget_by_id(id)
        except self.DOES_NOT_EXIST_ERROR:
            self._raise(self.NOT_FOUND_ERROR, id=id)

        return self.OUTPUT_DTO(**entity.snapshot)


class IAuthService(ABC):
    @abstractmethod
    async def authenticate(self, credentials: str): ...

    @abstractmethod
    async def verify(self, token: str): ...

    @abstractmethod
    def refresh_token(self, user: [Entity]): ...
