from abc import abstractmethod, ABC
from typing import Optional, Any
from uuid import UUID


class IRepository(ABC):

    @classmethod
    @abstractmethod
    async def aget_by_id(cls, id: UUID) -> Optional[Any]:
        pass

    @classmethod
    @abstractmethod
    async def aget_all(
            cls,
            limit=100,
            offset=0,
    ) -> list[Any]:
        pass

    @classmethod
    @abstractmethod
    async def asave(cls, entity: Any) -> None:
        pass

    @classmethod
    @abstractmethod
    async def aupdate(cls, entity: Any) -> None:
        pass

    @classmethod
    @abstractmethod
    async def adelete(cls, entity: Any) -> None:
        pass

    @classmethod
    @abstractmethod
    async def aget_first_from_filter(cls, **kwargs) -> Any:
        pass

    @classmethod
    @abstractmethod
    async def aget_all_from_filter(cls, **kwargs) -> list[Any]:
        pass