from dataclasses import dataclass

from pydantic import EmailStr
from pydantic.typing import Optional


@dataclass(frozen=True)
class UserAuthInputDto:
    username: str
    password: str


@dataclass(frozen=True)
class UserCreateInputDto:
    username: str
    password: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None


@dataclass(frozen=True)
class UserOutputDto:
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None