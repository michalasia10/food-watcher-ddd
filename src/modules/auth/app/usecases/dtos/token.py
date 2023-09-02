from dataclasses import dataclass

from modules.auth.domain.value_objects import UserID


@dataclass
class TokenOutputDto:
    api_token: str
    user_id: UserID
