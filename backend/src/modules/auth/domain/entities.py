from dataclasses import dataclass, field, fields
from typing import NoReturn

from foundation.domain.entity import Entity
from foundation.domain.value_objects import UUID

ANONYMOUS_ID = UUID("00000000-0000-0000-0000-000000000000")


@dataclass
class User(Entity):
    id: UUID = field(hash=True)
    username: str
    password: str = ""
    email: str = ""
    hashed_psw: str = ""
    first_name: str | None = ""
    last_name: str | None = ""
    is_super: bool = False
    is_active: bool = False

    @classmethod
    def create_anonymous(cls):
        return User(
            id=ANONYMOUS_ID,
            username='anonymous'
        )

    def _validate_fields(self, **kwargs) -> NoReturn:
        if unknown_kwargs := [kwarg_field not in fields(self) for kwarg_field in kwargs.keys()]:
            raise ValueError(f"You're trying to update unknown fields: {', '.join(unknown_kwargs)}")

    def update(self, **kwargs) -> NoReturn:
        self._validate_fields(**kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)
        # TODO: add logger

    def activate(self) -> NoReturn:
        self.is_active = True

    def add_superpow(self) -> NoReturn:
        self.is_super = True
