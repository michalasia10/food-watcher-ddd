import uuid
from typing import Any

from sqlalchemy import MetaData, Table, Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import as_declarative, registry

metadata = MetaData()
mapper_registry = registry(metadata=metadata)


@as_declarative(metadata=metadata)
class Base:
    __table__: Table

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        ...
