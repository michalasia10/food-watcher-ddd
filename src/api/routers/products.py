from classy_fastapi import get
from dependency_injector.wiring import inject
from fastapi import HTTPException
from starlette import status

from api.routers.base import BaseModelView
from api.shared import dependency
from config.di import Container
from modules.products.app.usecases.dtos.product import ProductOutputDto, ProductInputDto
from modules.products.app.usecases.query.product import ProductQuery


class ProductViewSet(BaseModelView[ProductInputDto, ProductOutputDto]):
    prefix = "/products"
    tag = "products"
    crud_methods = ("create", "list", "read")

    @inject
    def __init__(
        self,
        query_service=dependency(Container.product_query),
        command_service=dependency(Container.product_command),
    ) -> None:
        super(ProductViewSet, self).__init__(
            query_service=query_service,
            command_service=command_service,
            basic_create_dto=ProductInputDto,
            basic_output_dto=ProductOutputDto,
        )

    @get("/by_name/{name}")
    @inject
    def get_by_name(
        self,
        name: str,
        skip: int = 0,
        limit: int = 10,
        query_service: ProductQuery = dependency(Container.product_query),
    ) -> list[ProductOutputDto]:

        try:
            return query_service.get_by_name(name, skip, limit)
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)
