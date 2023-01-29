from dataclasses import dataclass

from pydantic import EmailStr
from pydantic.typing import Optional


@dataclass
class UserAuthInputDto:
    username: str
    password: str


@dataclass
class UserCreateInputDto:
    username: str
    password: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
