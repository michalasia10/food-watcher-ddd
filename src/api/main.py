from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from api.routers import (
    UserViewSet,
    ProductViewSet,
    ChatRouter,
    ChannelsViewSet,
    ConsumptionRouter,
    RecipeViewSet,
    RecipeProductViewSet,
)
from config import TORTOISE_CONFIG, settings
from config.api_config import ApiConfig
from config.container_ioc import Container
from src.api.setup import include_routers

####################################
######### Container CONFIG #########
####################################

container = Container()

container.config.from_dict(ApiConfig().model_dump())
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

