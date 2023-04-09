from dataclasses import dataclass

from pydantic import EmailStr
from pydantic.typing import Optional

from src.modules.auth.domain.value_objects import UserID


@dataclass(frozen=True)
class BaseUserDto:
    username: str
    password: str


@dataclass(frozen=True)
class UserAuthInputDto(BaseUserDto):
    ...


@dataclass(frozen=True)
class UserInputDto(BaseUserDto):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None


@dataclass(frozen=True)
class UserOutputDto:
    id: UserID
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
