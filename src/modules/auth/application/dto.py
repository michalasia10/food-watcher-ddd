from typing import Optional
from uuid import UUID

from pydantic import EmailStr, BaseModel

from src.modules.auth.domain.enums import GenderEnum


class BaseUserDto(BaseModel):
    username: str
    password: str


class UserAuthInputDto(BaseUserDto): ...


class MacroDto(BaseModel):
    proteins: float
    fats: float
    carbs: float
    calories: float


class UserSettingsBaseDto(BaseModel):
    age: int
    gender: GenderEnum = GenderEnum.UNSPECIFIED


class UserSettingsDto(UserSettingsBaseDto):
    macro: Optional[MacroDto] = None


class UserSettingsUpdateDto(BaseModel):
    age: Optional[int] = None
    gender: Optional[GenderEnum] = None
    macro: Optional[MacroDto] = None


class UserInputDto(BaseUserDto):
    email: EmailStr
    settings: UserSettingsDto
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserUpdateDto(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserOutputDto(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    settings: Optional[UserSettingsDto] = None


class TokenOutputDto(BaseModel):
    api_token: str
    user_id: UUID
