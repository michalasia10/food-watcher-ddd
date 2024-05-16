from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from tortoise.contrib.fastapi import register_tortoise

from src.api.response import ErrorResponse
from src.api.setup import include_routers
from src.config import TORTOISE_CONFIG, settings
from src.config.di import AppContainer
from src.core_new.domain.errors import Error
from src.modules.auth_new.controller import UserViewSet

####################################
######### Container CONFIG #########
####################################

container = AppContainer()
container.wire(
    modules=[
        # "api.routers.users",
        "src.modules.auth_new.controller",
        # "api.routers.products",
        # "api.routers.base",
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
        # ProductViewSet(),
        UserViewSet(),
        # ChannelsViewSet(),
        # ChatRouter,
        # ConsumptionRouter,
        # RecipeViewSet(),
        # RecipeProductViewSet(),
    ],
)


####################################
######## App Exception Handlers ###
####################################

@app.exception_handler(Error)
async def default_handler(request: Request, exc: Error) -> ErrorResponse:
    return ErrorResponse(
        status_code=exc.status_code,
        message=exc.message
    )


@app.exception_handler(Exception)
async def unknown_exception_handler(request: Request, exc: Exception) -> ErrorResponse:
    return ErrorResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        message="Unknown error occurred. Please try again later or create issue ticket."
    )


####################################
######## App Middlewares ###
####################################


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


####################################
############## END #################
####################################
