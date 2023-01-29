import uuid
from dataclasses import dataclass, field

from foundation.domain.entity import Entity
from foundation.domain.value_objects import UUID
from foundation.utils.functional import hash_helper


@dataclass
class User(Entity):
    id: UUID = field(hash=True, default_factory=lambda: uuid.uuid4())
    username: str = ""
    password: str = ""
    email: str = ""
    first_name: str | None = ""
    last_name: str | None = ""
    is_superuser: bool = False
    is_active: bool = False

    def hash_pswd(self):
        self.password = hash_helper.hash(self.password)