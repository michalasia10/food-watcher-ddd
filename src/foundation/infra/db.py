import uuid
from enum import Enum
from typing import Any

from flask_babel import lazy_gettext as _
from sqlalchemy import MetaData, Table, Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import as_declarative, registry

metadata = MetaData()
mapper_registry = registry(metadata=metadata)


class LabeledEnum(Enum):
    def __str__(self):
        return self.label

    def __getattr__(self, name):
        if name == 'label':
            try:
                return self._value_[1]
            except TypeError:
                return str(self.value)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    @classmethod
    def _missing_(cls, value):
        raise ValueError(f'{value} is not a valid {cls.__name__.lower()}')

    @classmethod
    def _generate_next_value_(cls, name, start, count, last_values):
        value = name.lower()
        return (value, _(name))


@as_declarative(metadata=metadata)
class Base:
    __table__: Table

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        ...

    class Meta:
        children = []
