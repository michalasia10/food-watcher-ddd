from typing import Any, NoReturn

from modules.auth.app.repository.user import UserRepository
from modules.auth.domain.value_objects import UserID
from src.foundation.infrastructure.repository import Repository
from src.modules.auth.domain.entities import User
from src.modules.auth.infra.models.user import User as UserModel


class SqlUserRepository(Repository, UserRepository):
    model = UserModel

    def get_by_id(self, id: UserID) -> User:
        return self.session.query(self.model).filter_by(id=str(id)).first()


    def create(self, entity: User) -> NoReturn:
        self.session.add(self.model(**entity.dict()))

    def update(self, entity: User):
        raise NotImplementedError

    def get_by_field_value(self, field: str, value: Any) -> User:
        return self.session.query(self.model).filter_by(**{field: value}).first()

    def delete(self, id: UserID) -> NoReturn:
        raise NotImplementedError

    def exists(self, field: str, value: Any) -> bool:
        return bool(self.session.query(self.model).filter_by(**{field: value}).first())
