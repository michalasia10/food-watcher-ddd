import time

from fastapi import FastAPI, Request

from api.routers import (
    UserViewSet,
    ProductViewSet,
    ChatRouter,
    ChannelsViewSet,
    ConsumptionRouter,
    RecipeViewSet
)
from config.api_config import ApiConfig
from config.container_ioc import Container
from src.api.setup import include_routers
from src.api.shared.utils import CurrentUser
from src.foundation.infra.request_context import request_context

container = Container()
container.config.from_pydantic(ApiConfig())
container.wire(
    modules=[
        'api.routers.users',
        'api.shared.auth',
        'api.routers.products',
        'api.routers.base',
        'api.routers.chat',
        'api.routers.consumption',
        'api.routers.recipe',
    ]
)

app = FastAPI()
include_routers(
    app,
    [
        ProductViewSet(),
        UserViewSet(),
        ChannelsViewSet(),
        ChatRouter,
        ConsumptionRouter,
        RecipeViewSet()
    ]
)
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
