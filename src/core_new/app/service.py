from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


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


class IAuthService(ABC):

    @abstractmethod
    async def authenticate(self, credentials: str): ...

    @abstractmethod
    async def verify(self, token: str): ...
