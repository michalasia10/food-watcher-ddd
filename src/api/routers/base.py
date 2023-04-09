import dataclasses
from functools import partial
from typing import Any, Type, Tuple, Dict, cast, Literal
from typing import List, TypeVar, Generic

from classy_fastapi.route_args import EndpointDefinition
from dependency_injector.wiring import inject
from fastapi import HTTPException, APIRouter, Response, Query, Depends
from fastapi import status
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from api.shared.auth import bearer_auth
from api.shared.filters.filters import BaseFilter
from api.shared.filters.validator import QueryValidator
from src.foundation.application.commands import CommandBase
from src.foundation.application.queries import QueryBase
from src.foundation.domain.value_objects import UUID

OutPutModel = TypeVar("OutPutModel", bound=BaseModel)
InPutModel = TypeVar("InPutModel", bound=BaseModel)


class RoutableMetav2(type):
    """This is a meta-class that converts all the methods that were marked by a route/path decorator into values on a
    class member called _endpoints that the Routable constructor then uses to add the endpoints to its router."""

    def __new__(cls: Type[type], name: str, bases: Tuple[Type[Any]], attrs: Dict[str, Any],
                **kwargs) -> 'RoutableMetav2':
        endpoints: List[EndpointDefinition] = []

        for v in attrs.values():
            if hasattr(v, '_endpoint'):
                endpoints.append(v._endpoint)

        attrs['_endpoints'] = endpoints
        return cast(RoutableMetav2, type.__new__(cls, name, bases, attrs))


CRUD_METHODS = Literal['create', 'list', 'delete', 'read']


class BaseModelView(Generic[OutPutModel, InPutModel], metaclass=RoutableMetav2):
    """ Class which prepare basic CRUD endpoints based on command / query service."""

    _endpoints: List[EndpointDefinition] = []
    tag: str | None = None
    prefix: str | None = None
    extra_router_kwargs: dict = {}
    crud_methods: tuple[CRUD_METHODS] = ('create', 'list', 'delete', 'read')

    @inject
    def __init__(self,
                 query_service: QueryBase,
                 command_service: CommandBase,
                 basic_create_dto: Generic[OutPutModel],
                 basic_output_dto: Generic[InPutModel],
                 filter_validator: QueryValidator | None = None) -> None:
        self._query_service = query_service
        self._command_service = command_service
        self.basic_output_dto = basic_output_dto
        self.basic_create_dto = basic_create_dto
        self._filter_validator = filter_validator or QueryValidator(BaseFilter)
        self.router = APIRouter(prefix=self.prefix, tags=[self.tag], **self.extra_router_kwargs)
        for endpoint in self._endpoints:
            self.router.add_api_route(endpoint=partial(endpoint.endpoint, self),
                                      **dataclasses.asdict(endpoint.args))
        self.register_basic_crud_endpoints(basic_create_dto)

    def register_basic_crud_endpoints(self, basic_create_dto):
        if 'list' in self.crud_methods:
            @self.router.get("/", response_model=List[self.basic_output_dto])
            def list(skip: int = 0,
                     limit: int = 100,
                     filter: str | None = Query(alias='filter', default=None, max_length=50)):
                """Basic endpoint to get list of instance. You can also use ?filter"""
                _filter = self._filter_validator.validate(filter)
                try:
                    return self._query_service.get_all(skip, limit)
                except Exception as e:
                    raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)

        if 'create' in self.crud_methods:
            @self.router.post("/", response_model=self.basic_output_dto)
            def create(item: basic_create_dto):
                """Basic endpoint to create instance"""
                try:
                    return self._command_service.create(item)
                except Exception as e:
                    raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)

        if 'read' in self.crud_methods:
            @self.router.get("/{id}", response_model=self.basic_output_dto)
            def read(id: UUID):
                """Basic endpoint to get instance by id."""
                item = self._query_service.get_by_id(id)
                if item is None:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
                return item

        if 'list' in self.crud_methods:
            @self.router.put("/{id}", response_model=self.basic_output_dto)
            def update(id: UUID, item: basic_create_dto, user: HTTPBearer = Depends(bearer_auth)):
                """Basic endpoint to update instance."""
                try:
                    return self._command_service.update(id, item)
                except Exception as e:
                    raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)

        if 'delete' in self.crud_methods:
            @self.router.delete("/{id}")
            def delete(id: UUID, user: HTTPBearer = Depends(bearer_auth)):
                "Basic endpoint to delete instance by id."
                try:
                    self._command_service.delete(id)
                except Exception as e:
                    raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)
                return Response(status.HTTP_204_NO_CONTENT)
