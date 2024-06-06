import dataclasses
from functools import partial
from http import HTTPStatus
from typing import List, TypeVar, Generic, Any, Tuple, Dict, cast, Literal, Type
from uuid import UUID

from classy_fastapi.route_args import EndpointDefinition
from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from src.core_new.app.service import ICrudService, IAuthService
from src.core_new.controller.auth import AuthController

OutPutModel = TypeVar("OutPutModel", bound=BaseModel)
InPutModel = TypeVar("InPutModel", bound=BaseModel)


class RoutableMetav2(type):
    """This is a metaclass that converts all the methods that were marked by a route/path decorator into values on a
    class member called _endpoints that the Routable constructor then uses to add the endpoints to its router.
    """

    def __new__(
            cls: Type[type],
            name: str,
            bases: Tuple[Type[Any]],
            attrs: Dict[str, Any],
            **kwargs
    ) -> "RoutableMetav2":
        endpoints: List[EndpointDefinition] = []

        for v in attrs.values():
            if hasattr(v, "_endpoint"):
                endpoints.append(v._endpoint)

        attrs["_endpoints"] = endpoints
        return cast(RoutableMetav2, type.__new__(cls, name, bases, attrs))


CRUD_METHODS = Literal["create", "list", "delete", "read", "update"]


class BaseModelView(Generic[OutPutModel, InPutModel], metaclass=RoutableMetav2):
    """Class which prepare basic CRUD endpoints based on command / query service."""

    _endpoints: List[EndpointDefinition] = []
    tag: str | None = None
    prefix: str | None = None
    extra_router_kwargs: dict = {}
    crud_methods: tuple[CRUD_METHODS] = ("create", "list", "delete", "read", "update")

    @inject
    def __init__(
            self,
            crud_service: ICrudService = None,
            auth_service: IAuthService = None,
            create_dto: OutPutModel | None = None,
            update_dto: OutPutModel | None = None,
            output_dto: InPutModel | None = None,
    ) -> None:
        self._service = crud_service
        self._auth_service = AuthController(auth_service)
        self.output_dto = output_dto
        self.create_dto = create_dto
        self.update_dto = update_dto
        self._router = APIRouter(
            prefix=self.prefix, tags=[self.tag], **self.extra_router_kwargs
        )
        for endpoint in self._endpoints:
            self.router.add_api_route(
                endpoint=partial(endpoint.endpoint, self),
                **dataclasses.asdict(endpoint.args)
            )
        self.register_basic_crud_endpoints(create_dto, update_dto)

    @property
    def router(self):
        return self._router

    def register_basic_crud_endpoints(self, basic_create_dto, basic_update_dto):

        if "list" in self.crud_methods:
            assert self.output_dto is not None and self._service is not None

            @self.router.get("/", response_model=List[self.output_dto])
            async def list(
                    skip: int = 0,
                    limit: int = 100,
            ):
                """Basic endpoint to get list of instance. You can also use ?filter"""
                return await self._service.get_all(skip, limit)

        if "create" in self.crud_methods:
            assert self.create_dto is not None and self._service is not None

            @self.router.post("/", response_model=self.output_dto, status_code=HTTPStatus.CREATED)
            async def create(item: basic_create_dto):
                """Basic endpoint to create instance"""

                return await self._service.create(item)

        if "read" in self.crud_methods:
            assert self.output_dto is not None and self._service is not None

            @self.router.get("/{id}", response_model=self.output_dto, status_code=HTTPStatus.OK)
            async def read(id: UUID):
                """Basic endpoint to get instance by id."""
                return await self._service.get_by_id(id)

        if "update" in self.crud_methods:
            assert self.create_dto is not None and self._service is not None

            @self.router.put("/{id}", response_model=self.output_dto, status_code=HTTPStatus.OK)
            async def update(
                    id: UUID,
                    item: basic_update_dto,
                    user: HTTPBearer = Depends(self._auth_service.bearer_auth),
            ):
                """Basic endpoint to update instance."""

                return await self._service.update(id, item, user_id=user.id, is_admin=user.is_admin)

        if "delete" in self.crud_methods:
            @self.router.delete("/{id}", status_code=HTTPStatus.NO_CONTENT)
            async def delete(id: UUID, user: HTTPBearer = Depends(self._auth_service.bearer_auth)):
                "Basic endpoint to delete instance by id."
                return await self._service.delete(id, user_id=user.id, is_admin=user.is_admin)
