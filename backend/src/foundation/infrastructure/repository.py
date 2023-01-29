from contextvars import ContextVar

from sqlalchemy.orm import Session


class Repository:
    model = NotImplementedError

    def __init__(self, db_session: ContextVar):
        self._session = db_session

    @property
    def session(self) -> Session:
        return self._session.get()
