from http import HTTPStatus
from uuid import UUID

from classy_fastapi import delete, post, get, put
from dependency_injector.wiring import inject
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.config.di import AppContainer
from src.core.app.service import IAuthService
from src.core.controller.crud import BaseModelView
from src.core.controller.di import dependency
from src.modules.recipe.application.dto.recipe import (
    RecipeInputDto,
    RecipeOutputDto,
    RecipeUpdateDto,
)
from src.modules.recipe.application.dto.recipe_product import (
    ProductForRecipeUpdateDto,
    ProductForRecipeInputDto,
)
from src.modules.recipe.application.service import RecipeService


class RecipeViewSet(BaseModelView[RecipeInputDto, RecipeOutputDto]):
    prefix = "/recipes"
    tag = "recipes"
    crud_methods = ("create_auth", "list", "read", "delete", "update")

    @inject
    def __init__(
        self,
        crud_service=dependency(AppContainer.recipe.service),
        auth_service=dependency(AppContainer.auth.auth_service),
    ) -> None:
        super(RecipeViewSet, self).__init__(
            crud_service=crud_service,
            auth_service=auth_service,
            create_dto=RecipeInputDto,
            update_dto=RecipeUpdateDto,
            output_dto=RecipeOutputDto,
        )

    @get("/all_my_recipes/")
    @inject
    async def get_all_my_recipes(
        self,
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
        service: RecipeService = dependency(AppContainer.recipe.service),
        auth_service: IAuthService = dependency(AppContainer.auth.auth_service),
    ) -> list[RecipeOutputDto]:
        """
        Get all recipes for a user.
        """
        user = await auth_service.verify(token.credentials)
        return await service.get_all_my_recipes(user_id=user.id)

    @post("/product_for_recipe/{recipe_id}/")
    @inject
    async def add_product_to_recipe(
        self,
        recipe_id: UUID,
        input_dto: ProductForRecipeInputDto,
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
        service: RecipeService = dependency(AppContainer.recipe.service),
        auth_service: IAuthService = dependency(AppContainer.auth.auth_service),
    ) -> RecipeOutputDto:
        """
        Add a product to a recipe.
        """
        user = await auth_service.verify(token.credentials)
        return await service.add_product(id=recipe_id, input_dto=input_dto, user_id=user.id, is_admin=user.is_admin)

    @put("/product_for_recipe/{product_id}/")
    @inject
    async def update_recipe_product(
        self,
        product_id: UUID,
        update_dto: ProductForRecipeUpdateDto,
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
        service: RecipeService = dependency(AppContainer.recipe.service),
        auth_service: IAuthService = dependency(AppContainer.auth.auth_service),
    ) -> RecipeOutputDto:
        """
        Update a product for a recipe.
        """
        user = await auth_service.verify(token.credentials)
        return await service.update_product(
            id=product_id,
            update_dto=update_dto,
            user_id=user.id,
            is_admin=user.is_admin,
        )

    @delete("/product_for_recipe/{product_id}/", status_code=HTTPStatus.NO_CONTENT)
    @inject
    async def delete_recipe_product(
        self,
        product_id: UUID,
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
        service: RecipeService = dependency(AppContainer.recipe.service),
        auth_service: IAuthService = dependency(AppContainer.auth.auth_service),
    ):
        """
        Delete a product from a recipe.
        """
        user = await auth_service.verify(token.credentials)
        return await service.delete_product(id=product_id, user_id=user.id, is_admin=user.is_admin)
