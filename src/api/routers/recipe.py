from dependency_injector.wiring import inject

from api.routers.base import BaseModelView
from api.shared import dependency
from config.container_ioc import Container
from modules.recipes.app.usecases.dtos.recipe import (
    RecipeInputDto,
    RecipeOutputDto,
    RecipeProductOutputDto,
    RecipeProductInputDto
)


class RecipeViewSet(BaseModelView[RecipeInputDto, RecipeOutputDto]):
    prefix = '/recipes'
    tag = 'recipes'
    crud_methods = ('create', 'list', 'read')

    @inject
    def __init__(
            self,
            query_service=dependency(Container.recipe_query),
            command_service=dependency(Container.recipe_command)
    ) -> None:
        super(RecipeViewSet, self).__init__(
            query_service=query_service,
            command_service=command_service,
            basic_create_dto=RecipeInputDto,
            basic_output_dto=RecipeOutputDto
        )


class RecipeProductViewSet(BaseModelView[RecipeProductInputDto, RecipeProductOutputDto]):
    prefix = '/recipe-products'
    tag = 'recipe-products'
    crud_methods = ('update','delete')

    @inject
    def __init__(
            self,
            query_service=dependency(Container.recipe_product_query),
            command_service=dependency(Container.recipe_product_command)
    ) -> None:
        super(RecipeProductViewSet, self).__init__(
            query_service=query_service,
            command_service=command_service,
            basic_create_dto=RecipeProductInputDto,
            basic_output_dto=RecipeProductOutputDto
        )
