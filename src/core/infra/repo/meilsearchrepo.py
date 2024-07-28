from contextlib import asynccontextmanager
from typing import Any
from uuid import UUID

from loguru import logger
from meilisearch_python_sdk import AsyncClient, AsyncIndex
from meilisearch_python_sdk.models.search import SearchResults

from src.core.domain.repo.search_engine import ISearchRepository
from src.core.utils.encoder import CustomJsonEncoder


class MeiliSearchRepository(ISearchRepository):
    """
    Meilisearch repository class as a search engine.

    https://www.meilisearch.com/
    """

    INDEX: str = ""
    SEARCH_FIELDS: list[str] | None = None
    FIELDS_TO_GET: list[str] | None = None

    def __init__(self, meilisearch_url: str, meilisearch_master_key: str):
        self._meilisearch_url = meilisearch_url
        self._meilisearch_master_key = meilisearch_master_key

    @asynccontextmanager
    async def _client(self) -> AsyncClient:
        client = AsyncClient(
            url=self._meilisearch_url,
            api_key=self._meilisearch_master_key,
        )
        try:
            yield client
        finally:
            await client.aclose()

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
        """
        Search for documents in the Meilisearch index.

        Returns: list[Any]

        """

        async with self._client() as client:
            index: AsyncIndex = await self.aget_create_index(client=client)
            result: SearchResults = await index.search(
                query=query,
                offset=offset,
                limit=limit,
                attributes_to_retrieve=self.FIELDS_TO_GET or fields_to_get,
                attributes_to_search_on=self.SEARCH_FIELDS or search_fields,
            )

        result_hints = result.hits

        logger.info("Search result count: {result}", result=len(result_hints))
        return result_hints

    async def aget_create_index(
        self,
        client: AsyncClient,
        *args,
        **kwargs,
    ) -> AsyncIndex:
        return await client.get_or_create_index(
            uid=self.INDEX,
            primary_key="id",
        )

    async def acreate_document(self, document: dict, *args, **kwargs) -> None:
        """
        Create a document in the Meilisearch index.

        Args:
            document: dict: The document to be created.

        Returns: None

        """
        async with self._client() as client:
            index: AsyncIndex = await self.aget_create_index(client=client)

            await index.add_documents(
                documents=[document],
                primary_key="id",
                serializer=CustomJsonEncoder,
            )
            logger.info("Document created.")

    async def adelete_document(self, document_id: UUID, *args, **kwargs) -> None:
        """
        Delete a document from the Meilisearch index.

        Args:
            document_id: UUID: The id of the document to be deleted.

        Returns: None

        """
        async with self._client() as client:
            index: AsyncIndex = await self.aget_create_index(client=client)

            await index.delete_document(document_id=str(document_id))
            logger.info(
                "Document with {document_id} id deleted.", document_id=document_id
            )

    async def aupdate_document(
        self,
        document_id: UUID,
        document: dict,
        *args,
        **kwargs,
    ) -> None:
        """
        Update a document in the Meilisearch index.

        Args:
            document_id: UUID: The id of the document to be updated.
            document: The document to be updated.

        Returns: None

        """
        async with self._client() as client:
            index: AsyncIndex = await self.aget_create_index(client=client)
            await index.update_documents(
                documents=[document], primary_key="id", serializer=CustomJsonEncoder
            )
            logger.info("Document updated {document_id}.", document_id=document_id)
