from pydantic.dataclasses import dataclass

from src.foundation.domain.entities import AggregateRoot
# from src.foundation.utils.functional import hash_helper


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
        pass
        # self.password = hash_helper.hash(self.password)
