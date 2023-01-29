from contextvars import ContextVar

from sqlalchemy.orm import Session

from src.foundation.domain.entities import Entity
from src.foundation.infrastructure.db import Base


class Repository:
    model = NotImplementedError

    def __init__(self, db_session: ContextVar):
        self._session = db_session

    @property
    def session(self) -> Session:
        return self._session.get()

    def data_to_entity(self, data: Base, entity: [Entity]):
        return entity(**data.__dict__)

    def entity_to_data(self, entity: [Entity]) -> [Base]:
        return self.model(**entity.to_dict())
