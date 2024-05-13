from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from api.routers import (
    ProductViewSet,
    ChatRouter,
    ChannelsViewSet,
    ConsumptionRouter,
    RecipeViewSet,
    RecipeProductViewSet,
)
from config import TORTOISE_CONFIG, settings
from config.di import AppContainer
from src.api.setup import include_routers
from src.modules.auth_new.controlers import UserViewSet

####################################
######### Container CONFIG #########
####################################

container = AppContainer()
container.wire(
    modules=[
        "api.routers.users",
        "api.shared.auth",
        "api.routers.products",
        "api.routers.base",
        "api.routers.chat",
        "api.routers.consumption",
        "api.routers.recipe",
    ]
)

####################################
######### FastAPI App Init #########
####################################

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=True
)

####################################
######### FastAPI Routers ##########
####################################

include_routers(
    app,
    [
        ProductViewSet(),
        UserViewSet(),
        ChannelsViewSet(),
        ChatRouter,
        ConsumptionRouter,
        RecipeViewSet(),
        RecipeProductViewSet(),
    ],
)
####################################
######## Registration Extra to App #
####################################

app.container = container
register_tortoise(
    app,
    config=TORTOISE_CONFIG,
    generate_schemas=False,
    add_exception_handlers=False,
)
# ToDo: Figure out middleware for ws
# ToDo: Add exception handlers


####################################
############## END #################
####################################
