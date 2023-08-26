from typing import Any

from fastapi import APIRouter
from fastapi import FastAPI

from api.routers import BaseModelView


def include_routers(app: FastAPI, routers: list[BaseModelView | APIRouter | Any]):
    router: BaseModelView | APIRouter
    for router in routers:
        if isinstance(router, BaseModelView):
            app.include_router(router.router)
        elif isinstance(router, APIRouter):
            app.include_router(router)
        else:
            raise Exception("Invalid router type")
