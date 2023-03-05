from dependency_injector.wiring import inject

from api.routers.base import BaseModelView
from api.shared import dependency
from config.container_ioc import Container
from modules.products.app.usecases.dtos.product import ProductOutputDto, ProductInputDto


class ProductViewSet(BaseModelView[ProductInputDto, ProductOutputDto]):
    prefix = '/products'
    tag = 'products'
    crud_methods = ('create', 'list', 'read')

    @inject
    def __init__(self, query_service=dependency(Container.product_query),
                 command_service=dependency(Container.product_command)):
        super(ProductViewSet, self).__init__(query_service=query_service,
                                             command_service=command_service,
                                             basic_create_dto=ProductInputDto,
                                             basic_output_dto=ProductOutputDto)
