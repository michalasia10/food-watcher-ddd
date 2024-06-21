from typing import Any

from fastapi import APIRouter
from fastapi import FastAPI

from src.core.controller.crud import BaseModelView


def include_routers(
    app: FastAPI, routers: list[BaseModelView | APIRouter | Any]
) -> None:
    """
    Include routers in the FastAPI app.

    Function can handle Type[BaseModelView] and get router from it, and also APIRouter.

    Args:
        app: FastAPI
        routers: list[BaseModelView | APIRouter | Any]

    Returns:

    """
    router: BaseModelView | APIRouter
    for router in routers:
        match router:
            case BaseModelView():
                app.include_router(router.router)
            case APIRouter():
                app.include_router(router)
            case _:
                raise Exception("Invalid router type")
