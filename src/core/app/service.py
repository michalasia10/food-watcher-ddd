from abc import ABC, abstractmethod
from typing import Optional, Type
from uuid import UUID

from loguru import logger
from pydantic import BaseModel

from src.core.domain.entity import Entity
from src.core.domain.errors import Error, NotSupportedError
from src.core.domain.repo.postgres import IPostgresRepository
from src.core.domain.repo.search_engine import ISearchRepository


class ICrudService(ABC):
    @abstractmethod
    async def create(
        self,
        input_dto: BaseModel,
        user_id: UUID = None,
        is_admin: bool = False,
    ):
        pass

    @abstractmethod
    async def get_all(
        self,
        skip: int,
        limit: int,
        query: str | None = None,
    ):
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID):
        pass

    @abstractmethod
    async def update(
        self,
        id: UUID,
        input_dto: BaseModel,
        user_id: Optional[UUID] = None,
        is_admin: bool = False,
    ):
        pass

    @abstractmethod
    async def delete(self, id: UUID, user_id: Optional[UUID] = None, is_admin: bool = False):
        pass


class BaseCrudService(ICrudService):
    OUTPUT_DTO: [BaseModel] = None
    NOT_RECORD_OWNER_ERROR = None
    NOT_FOUND_ERROR = None
    DOES_NOT_EXIST_ERROR = None
    FETCH_FIELDS = None

    def __init__(
        self,
        repository: [IPostgresRepository],
        search_repo: [ISearchRepository] = None,
    ):
        self._repository = repository
        self._search_repo: ISearchRepository = search_repo

    @abstractmethod
    async def create(self, input_dto, user_id: UUID = None, is_admin: bool = False): ...

    @staticmethod
    def _raise(error: tuple[Type[Error], str], id: UUID = None):
        _exception, msg = error
        raise _exception(msg.format(id=id) if "id" in msg else msg)

    async def update(self, id: UUID, input_dto: BaseModel, user_id: UUID = None, is_admin=False) -> BaseModel:
        entity: Entity = await self._repository.aget_by_id(id)

        if not is_admin and (
            (hasattr(entity, "user_id") and getattr(entity, "user_id") != user_id)
            or (hasattr(entity, "username") and getattr(entity, "id") != user_id)
        ):
            self._raise(self.NOT_RECORD_OWNER_ERROR, id=id)

        entity.update(input_dto)
        await self._repository.aupdate(entity)

        logger.info("Entity[{entity}] updated", entity=str(entity))
        fresh_entity: Entity = await self._repository.aget_by_id(
            id=id,
            fetch_fields=self.FETCH_FIELDS,
        )

        if self._search_repo:
            try:
                await self._search_repo.aupdate_document(
                    document_id=id,
                    document=fresh_entity.snapshot,
                )
            except Exception as e:
                logger.error(f"Error updating search index: {e}")

        return self.OUTPUT_DTO(**self._repository.convert_snapshot(fresh_entity.snapshot))

    async def delete(self, id: UUID, user_id: UUID = None, is_admin=False) -> None:
        entity: Entity = await self._repository.aget_by_id(id)

        if not is_admin and (
            (hasattr(entity, "user_id") and getattr(entity, "user_id") != user_id)
            or (hasattr(entity, "username") and getattr(entity, "id") != user_id)
        ):
            self._raise(self.NOT_RECORD_OWNER_ERROR, id=id)

        await self._repository.adelete(entity)
        logger.info("Entity[{entity}] deleted", entity=str(entity))

        if self._search_repo:
            try:
                await self._search_repo.adelete_document(document_id=id)
            except Exception as e:
                logger.error(f"Error deleting search index: {e}")

    async def get_all(
        self,
        skip: int,
        limit: int,
        query: str | None = None,
    ) -> list[BaseModel]:
        if query and not self._search_repo:
            raise NotSupportedError("Search is not implemented for this service.")

        if query:
            search_result = []

            try:
                search_result: list[dict] = await self._search_repo.asearch(query=query, offset=skip, limit=limit)
            except (Exception, Exception) as e:
                logger.error(f"Error searching: {e}")
                entities = await self._repository.aget_all(
                    offset=skip,
                    limit=limit,
                    fetch_fields=self.FETCH_FIELDS,
                )
            finally:
                entities: list[Entity] = await self._repository.aget_all_from_filter(
                    offset=skip,
                    limit=limit,
                    id__in=[result.get("id") for result in search_result],
                    fetch_fields=self.FETCH_FIELDS,
                )

        else:
            entities: list[Entity] = await self._repository.aget_all(
                offset=skip,
                limit=limit,
                fetch_fields=self.FETCH_FIELDS,
            )
        return [self.OUTPUT_DTO(**self._repository.convert_snapshot(entity.snapshot)) for entity in entities]

    async def get_by_id(self, id: UUID) -> BaseModel:
        try:
            entity: Entity = await self._repository.aget_by_id(
                id=id,
                fetch_fields=self.FETCH_FIELDS,
            )
        except self.DOES_NOT_EXIST_ERROR:
            self._raise(self.NOT_FOUND_ERROR, id=id)

        return self.OUTPUT_DTO(**self._repository.convert_snapshot(entity.snapshot))


class IAuthService(ABC):
    @abstractmethod
    async def authenticate(self, credentials: str): ...

    @abstractmethod
    async def verify(self, token: str): ...

    @abstractmethod
    def refresh_token(self, user: [Entity]): ...
