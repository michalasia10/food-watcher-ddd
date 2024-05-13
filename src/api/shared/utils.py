import asyncio
from uuid import uuid4

from pydantic import BaseModel

from foundation.domain.value_objects import UUID


async def get_event_loop():
    loop = asyncio.get_event_loop()
    yield loop


class CurrentUser(BaseModel):
    id: UUID
    username: str

    @classmethod
    def fake_user(cls):
        return CurrentUser(id=uuid4(), username="fake_user")
