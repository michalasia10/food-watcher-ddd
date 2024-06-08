# libs
from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from logfire import instrument_fastapi
from loguru import logger
from tortoise.contrib.fastapi import register_tortoise

# important stuff
from src.api.response import ErrorResponse
from src.api.router_util import include_routers
from src.config import TORTOISE_CONFIG, settings
from src.config.di import AppContainer
from src.core_new.domain.errors import Error
# controllers
from src.modules.auth_new.controller import UserViewSet
from src.modules.product_new.controller.consumption import router as consumption_router
from src.modules.product_new.controller.product import ProductViewSet
from src.modules.recipe_new.controller import RecipeViewSet

####################################
######### Container CONFIG #########
####################################

container = AppContainer()
container.wire(
    modules=[
        "src.modules.auth_new.controller",
        "src.modules.product_new.controller.product",
        "src.modules.product_new.controller.consumption",
        "src.modules.recipe_new.controller",
        # "api.routers.chat",
        # "api.routers.consumption",
        # "api.routers.recipe",
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
        # ViewSets
        UserViewSet(),
        ProductViewSet(),
        RecipeViewSet(),
        # Routers
        consumption_router,
        # ChannelsViewSet(),
        # ChatRouter,
        # RecipeViewSet(),
        # RecipeProductViewSet(),
    ],
)


####################################
######## App Exception Handlers ####
####################################

@app.exception_handler(Error)
async def default_handler(request: Request, exc: Error) -> ErrorResponse:
    return ErrorResponse(
        status_code=exc.status_code,
        message=exc.message
    )


@app.exception_handler(Exception)
async def unknown_exception_handler(request: Request, exc: Exception) -> ErrorResponse:
    logger.error(f"Unknown error occurred: {exc}", request=request)
    return ErrorResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        message="Unknown error occurred. Please try again later or create issue ticket."
    )


####################################
######## App Middlewares ###########
####################################


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ToDo: Figure out middleware for ws

####################################
######## Registration Extra to App #
####################################

###  Container DI ######
app.container = container

###  Tortoise ORM ######
register_tortoise(
    app,
    config=TORTOISE_CONFIG,
    generate_schemas=False,
    add_exception_handlers=False,
)
### LogFire ######

instrument_fastapi(app=app)

####################################
############## END #################
####################################
