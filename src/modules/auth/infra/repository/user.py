from typing import Any, NoReturn

from src.modules.auth.app.repository.user import UserRepository
from src.modules.auth.domain.value_objects import UserID
from src.foundation.infrastructure.repository import Repository
from src.modules.auth.domain.entities import User
from src.modules.auth.infra.models.user import User as UserModel


class SqlUserRepository(Repository, UserRepository):
    model = UserModel

    def get_by_id(self, id: UserID) -> User:
        return self.data_to_entity(self.session.query(self.model).filter_by(id=str(id)).first(), User)

    def create(self, entity: User) -> User:
        entity.hash_pswd()
        self.session.add(self.entity_to_data(entity))
        return entity

    def update(self, entity: User):
        raise NotImplementedError

    def get_by_field_value(self, field: str, value: Any) -> User:
        data = self.session.query(self.model).filter_by(**{field: value}).first()
        return self.data_to_entity(data, User)

    def delete(self, id: UserID) -> NoReturn:
        raise NotImplementedError

    def exists(self, field: str, value: Any) -> bool:
        return bool(self.session.query(self.model).filter_by(**{field: value}).first())

    def get_all(self) -> list[User]:
        data = self.session.query(self.model).all()
        return [self.data_to_entity(dat, User) for dat in data]

    def get_all_pagination(self, skip: int, limit: int) -> list[User]:
        data = self.session.query(self.model).offset(skip).limit(limit).all()
        return [self.data_to_entity(dat, User) for dat in data]
