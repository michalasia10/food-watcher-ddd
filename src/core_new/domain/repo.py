from abc import abstractmethod, ABC
from typing import Optional, Any
from uuid import UUID


class IRepository(ABC):

    @classmethod
    @abstractmethod
    async def aget_by_id(cls, id: UUID, *args, **kwargs) -> Optional[Any]:
        pass

    @classmethod
    @abstractmethod
    async def aget_all(
            cls,
            limit=100,
            offset=0,
            *args,
            **kwargs
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
    async def aget_first_from_filter(cls, *args, **kwargs) -> Any:
        pass

    @classmethod
    @abstractmethod
    async def aget_all_from_filter(cls, *args, **kwargs) -> list[Any]:
        pass
