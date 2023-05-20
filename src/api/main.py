import time

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

from api.routers.chat import chat_router, ChannelsViewSet
from api.routers.products import ProductViewSet
from api.routers.users import UserViewSet
from api.shared.utils import CurrentUser
from config.api_config import ApiConfig
from config.container_ioc import Container
from src.foundation.infrastructure.request_context import request_context

container = Container()
container.config.from_pydantic(ApiConfig())
container.wire(
    modules=['api.routers.users',
             'api.shared.auth',
             'api.routers.products',
             'api.routers.base',
             'api.routers.chat']
)

app = FastAPI()

app.include_router(ProductViewSet().router)
app.include_router(UserViewSet().router)
app.include_router(chat_router)
app.include_router(ChannelsViewSet().router)
app.container = container


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


class WebSocketMiddleware:
    def __init__(self, app):
        self.app = app

    def run_websocket_session(self):
        request_context.begin_request(current_user=CurrentUser.fake_user())

    def end_websocket_session(self):
        request_context.end_request()

    async def __call__(self, scope, receive, send):
        if scope['type'] == 'websocket':
            self.run_websocket_session()

        await self.app(scope, receive, send)

        if scope['type'] == 'websocket':
            self.end_websocket_session()


app.add_middleware(WebSocketMiddleware)
