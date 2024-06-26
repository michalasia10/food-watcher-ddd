from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class ISearchRepository(ABC):
    @abstractmethod
    async def asearch(
        self,
        query: str,
        offset: int = 0,
        limit: int = 100,
        fields_to_get: list[str] | None = None,
        search_fields: list[str] | None = None,
        *args,
        **kwargs,
    ) -> list[Any]:
        pass

    @abstractmethod
    async def aget_create_index(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    async def acreate_document(
        self,
        document: dict,
        *args,
        **kwargs,
    ) -> None:
        pass

    @abstractmethod
    async def adelete_document(
        self,
        document_id: UUID,
        *args,
        **kwargs,
    ) -> None:
        pass

    @abstractmethod
    async def aupdate_document(
        self,
        document_id: UUID,
        document: dict,
        *args,
        **kwargs,
    ) -> None:
        pass
