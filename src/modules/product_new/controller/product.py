from dependency_injector.wiring import inject

from src.api.shared import dependency
from src.config.di import AppContainer
from src.core_new.controller.crud import BaseModelView
from src.modules.product_new.application.dto.product import ProductInputDto, ProductOutputDto


class ProductViewSet(BaseModelView[ProductInputDto, ProductOutputDto]):
    prefix = "/products"
    tag = "products"
    crud_methods = ("create", "list", "read")

    @inject
    def __init__(
            self,
            crud_service=dependency(AppContainer.product.product_service),
            auth_service=dependency(AppContainer.auth.auth_service),
    ) -> None:
        super(ProductViewSet, self).__init__(
            crud_service=crud_service,
            auth_service=auth_service,
            create_dto=ProductInputDto,
            update_dto=ProductInputDto,
            output_dto=ProductOutputDto,
        )
