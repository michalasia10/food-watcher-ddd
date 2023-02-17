from typing import Optional

from pydantic import BaseModel, EmailStr


class BaseFilter(BaseModel):
    id: Optional[int] = None


class UserFilter(BaseFilter):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
