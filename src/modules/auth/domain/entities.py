from pydantic.dataclasses import dataclass

from foundation.domain.entities import AggregateRoot
from foundation.utils.functional import hash_helper


@dataclass(kw_only=True)
class User(AggregateRoot):
    username: str = ""
    password: str = ""
    email: str = ""
    first_name: str | None = ""
    last_name: str | None = ""
    is_superuser: bool | None = False
    is_active: bool | None = False

    def hash_pswd(self):
        self.password = hash_helper.hash(self.password)
