import time
from uuid import uuid4, UUID

from fastapi import FastAPI, Request, Depends
from pydantic import BaseModel

from api.routers import auth
from config.api_config import ApiConfig
from config.container_ioc import Container
from foundation.infrastructure.request_context import request_context


container = Container()
container.config.from_pydantic(ApiConfig())
container.wire(modules=['api.routers.auth','api.shared.auth'])



app = FastAPI()

app.include_router(auth.router)
app.container = container


class CurrentUser(BaseModel):
    id: UUID
    username: str

    @classmethod
    def fake_user(cls):
        return CurrentUser(id=uuid4(), username="fake_user")


@app.middleware("http")
async def add_request_context(request: Request, call_next):
    start_time = time.time()
    request_context.begin_request(current_user=CurrentUser.fake_user())

    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    finally:
        request_context.end_request()
