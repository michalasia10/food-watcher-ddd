import time
from dataclasses import dataclass

import jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from src.core_new.domain.entity import Entity
from src.modules.auth_new.domain.enums import StatusEnum, TypeEnum

hash_helper = CryptContext(schemes=["bcrypt"])


@dataclass
class User(Entity):
    # ToDo: implement check rule ( Error copuled with BussinesRule ?? )
    username: str
    password: str
    email: str
    first_name: str | None = ""
    last_name: str | None = ""
    status: str = StatusEnum.INACTIVE.value
    type: str = TypeEnum.USER.value

    @property
    def is_admin(self) -> bool:
        return self.type == TypeEnum.ADMIN.value

    @staticmethod
    def _hash_pswd(password: str) -> str:
        return hash_helper.hash(password)

    @classmethod
    def create(
            cls,
            username: str,
            password: str,
            email: str,
            first_name: str = '',
            last_name: str = '',
            status: str = StatusEnum.INACTIVE.value,
            type: str = TypeEnum.USER.value,
    ) -> 'User':
        return cls(
            id=cls.create_id(),
            username=username,
            password=cls._hash_pswd(password),
            email=email,
            first_name=first_name,
            last_name=last_name,
            status=status,
            type=type,
            created_at=cls.create_now_time(),
            updated_at=cls.create_now_time(),
        )

    def correct_password(self, password: str) -> bool:
        return hash_helper.verify(
            secret=password,
            hash=self.password
        )

    def create_token(
            self,
            secret_key: str,
            algorithm: str,
    ) -> str:
        return jwt.encode(
            payload={
                "user_id": str(self.id),
                "expires": time.time() + 2400,
            },
            key=secret_key,
            algorithm=algorithm,
        )

    @staticmethod
    def get_user_filter_by_decoded_token(token: dict) -> dict:
        return dict(id=token.get("user_id"))

    def update(self, input_dto: BaseModel) -> 'Entity':
        if input_dto.password:
            input_dto.password = self._hash_pswd(input_dto.password)

        return super(User, self).update(input_dto)
