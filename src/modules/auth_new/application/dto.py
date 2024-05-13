from typing import Optional
from uuid import UUID

from pydantic import EmailStr, BaseModel


class BaseUserDto(BaseModel):
    username: str
    password: str


class UserAuthInputDto(BaseUserDto): ...


class UserInputDto(BaseUserDto):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserOutputDto(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class TokenOutputDto(BaseModel):
    api_token: str
    user_id: UUID
