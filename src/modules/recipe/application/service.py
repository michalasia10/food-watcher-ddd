from typing import Optional

from loguru import logger
from tortoise.exceptions import DoesNotExist
from uuid6 import UUID

from src.core.app.service import ICrudService
from src.core.domain.errors import Error
from src.core.domain.repo.postgres import IPostgresRepository
from src.core.domain.repo.search_engine import ISearchRepository
from src.modules.recipe.application.dto.recipe import (
    RecipeInputDto,
    RecipeOutputDto,
    RecipeUpdateDto,
)
from src.modules.recipe.application.dto.recipe_product import (
    ProductForRecipeInputDto,
    ProductForRecipeUpdateDto,
)
from src.modules.recipe.domain.entity.recipe import Recipe
from src.modules.recipe.domain.entity.recipe_product import ProductForRecipe
from src.modules.recipe.domain.errors import (
    RecipeNotFound,
    RecipeNotRecordOwner,
    ProductForRecipeNotFound,
    ProductForRecipeNotRecordOwner,
    ProductNotFound,
)


class RecipeService(ICrudService):
    """
    Service class for Recipe.
    """

    def __init__(
        self,
        product_service: [ICrudService],
        product_for_recipe_repository: [IPostgresRepository],
        recipe_repository: [IPostgresRepository],
        search_repo: [ISearchRepository],
    ):
        self._product_service: ICrudService = product_service
        self._product_for_recipe_repository: IPostgresRepository = (
            product_for_recipe_repository
        )
        self._recipe_repository: IPostgresRepository = recipe_repository
        self._search_repo: ISearchRepository = search_repo

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 10,
        query: str | None = None,
    ) -> [RecipeOutputDto]:
        search_result = []

        async def _get_recipes_normal_query():
            return await self._recipe_repository.aget_all(
                offset=skip,
                limit=limit,
                fetch_fields=["products_for_recipe", "products_for_recipe__product"],
            )

        def _convert_to_recipe_output_dto(_recipes):
            return [
                RecipeOutputDto(
                    **self._recipe_repository.convert_snapshot(snapshot=recipe.snapshot)
                )
                for recipe in _recipes
            ]

        if query:
            logger.info("Searching recipes with query: {query}", query=query)

            try:
                search_result = await self._search_repo.asearch(
                    offset=skip,
                    limit=limit,
                    query=query,
                )
            except (Exception, Error) as e:
                logger.error(f"Error while searching recipes: {e}")
                recipes = await self._recipe_repository.aget_all(
                    offset=skip,
                    limit=limit,
                    fetch_fields=[
                        "products_for_recipe",
                        "products_for_recipe__product",
                    ],
                )
                return _convert_to_recipe_output_dto(recipes)
            finally:
                logger.info("Recipes found: {recipes_id}", recipes_id=search_result)
                recipes = await self._recipe_repository.aget_all_from_filter(
                    offset=skip,
                    limit=limit,
                    id__in=[result.get("id") for result in search_result],
                    fetch_fields=[
                        "products_for_recipe",
                        "products_for_recipe__product",
                    ],
                )
                return _convert_to_recipe_output_dto(recipes)

        return [
            RecipeOutputDto(
                **self._recipe_repository.convert_snapshot(snapshot=recipe.snapshot)
            )
            for recipe in await _get_recipes_normal_query()
        ]

    async def get_all_my_recipes(
        self, user_id: UUID, skip: int = 0, limit: int = 10
    ) -> [RecipeOutputDto]:
        recipes = await self._recipe_repository.aget_all_from_filter(
            offset=skip,
            limit=limit,
            user_id=user_id,
            fetch_fields=["products_for_recipe", "products_for_recipe__product"],
        )

        return [
            RecipeOutputDto(
                **self._recipe_repository.convert_snapshot(snapshot=recipe.snapshot)
            )
            for recipe in recipes
        ]

    async def get_by_id(self, recipe_id: UUID) -> RecipeOutputDto:
        try:
            recipe = await self._recipe_repository.aget_by_id(
                id=recipe_id,
                fetch_fields=["products_for_recipe", "products_for_recipe__product"],
            )
        except DoesNotExist:
            raise RecipeNotFound(message=f"Recipe with id {recipe_id} not found.")
        return RecipeOutputDto(
            **self._recipe_repository.convert_snapshot(snapshot=recipe.snapshot)
        )

    async def create(
        self, input_dto: RecipeInputDto, user_id: UUID = None, **kwargs
    ) -> RecipeOutputDto:
        entity = Recipe.create(
            name=input_dto.name,
            link=input_dto.link,
            description=input_dto.description,
            user_id=user_id,
        )
        logger.info(
            "Count: {number} of product(s) for recipe: {recipe_id}",
            recipe_id=entity.id,
            number=len(input_dto.products),
        )
        await self._recipe_repository.asave(entity)

        try:
            await self._search_repo.acreate_document(document=entity.snapshot)
        except Exception as e:
            logger.error(
                "Error while creating document in search engine: {error}", error=e
            )

        for product_for_recipe in input_dto.products:
            try:
                product = await self._product_service.get_by_id(
                    id=product_for_recipe.product_id
                )
            except Error as e:
                raise ProductNotFound(message=e.message)

            product_for_recipe_entity = ProductForRecipe.create(
                recipe=entity,
                product=product,
                weight_in_grams=product_for_recipe.weight_in_grams,
            )
            await self._product_for_recipe_repository.asave(
                entity=product_for_recipe_entity
            )

        await self._recipe_repository.aupdate(
            entity=entity
        )  # ToDo: Add in future get_or_update

        recipe = await self._recipe_repository.aget_by_id(
            id=entity.id,
            fetch_fields=[
                "products_for_recipe",
                "products_for_recipe__product",
            ],
        )
        return RecipeOutputDto(
            **self._recipe_repository.convert_snapshot(snapshot=recipe.snapshot)
        )

    async def update(
        self,
        id: UUID,
        input_dto: RecipeUpdateDto,
        user_id: Optional[UUID] = None,
        is_admin: bool = False,
    ):
        try:
            recipe = await self._recipe_repository.aget_by_id(id)
        except DoesNotExist:
            raise RecipeNotFound(message=f"Recipe with id {id} not found.")

        if not is_admin and recipe.user_id != user_id:
            raise RecipeNotRecordOwner(
                message=f"Recipe with id {id} not owned by user with id {user_id}."
            )

        recipe.name = input_dto.name
        recipe.link = input_dto.link
        recipe.description = input_dto.description

        await self._recipe_repository.aupdate(recipe)

        try:
            await self._search_repo.aupdate_document(
                document_id=id,
                document={
                    key: value
                    for key, value in recipe.snapshot.items()
                    if key != "products_for_recipe"
                },
            )
        except Exception as e:
            logger.error(
                "Error while updating document in search engine: {error}", error=e
            )

        recipe = await self._recipe_repository.aget_by_id(
            id=recipe.id,
            fetch_fields=["products_for_recipe", "products_for_recipe__product"],
        )
        return RecipeOutputDto(
            **self._recipe_repository.convert_snapshot(snapshot=recipe.snapshot)
        )

    async def delete(
        self, id: UUID, user_id: Optional[UUID] = None, is_admin: bool = False
    ):
        try:
            recipe = await self._recipe_repository.aget_by_id(id)
        except DoesNotExist:
            raise RecipeNotFound(message=f"Recipe with id {id} not found.")

        if not is_admin and recipe.user_id != user_id:
            raise RecipeNotRecordOwner(
                message=f"Recipe with id {id} not owned by user with id {user_id}."
            )

        await self._recipe_repository.adelete(recipe)

        try:
            await self._search_repo.adelete_document(document_id=recipe.id)
        except Exception as e:
            logger.error(
                "Error while deleting document in search engine: {error}", error=e
            )

    async def add_product(
        self,
        id: UUID,
        input_dto: ProductForRecipeInputDto,
        user_id: Optional[UUID] = None,
        is_admin: bool = False,
    ) -> RecipeOutputDto:
        try:
            recipe = await self._recipe_repository.aget_by_id(id)
        except DoesNotExist:
            raise RecipeNotFound(message=f"Recipe with id {id} not found.")

        if not is_admin and recipe.user_id != user_id:
            raise ProductForRecipeNotRecordOwner(
                message=f"Recipe with id {id} not owned by user with id {user_id}."
            )

        try:
            product = await self._product_service.get_by_id(input_dto.product_id)
        except Error as e:
            raise ProductNotFound(message=e.message)

        product_for_recipe = ProductForRecipe.create(
            recipe=recipe,
            product=product,
            weight_in_grams=input_dto.weight_in_grams,
        )
        await self._product_for_recipe_repository.asave(product_for_recipe)
        await self._recipe_repository.aupdate(recipe)

        recipe = await self._recipe_repository.aget_by_id(
            id=recipe.id,
            fetch_fields=["products_for_recipe", "products_for_recipe__product"],
        )

        return RecipeOutputDto(
            **self._recipe_repository.convert_snapshot(snapshot=recipe.snapshot)
        )

    async def update_product(
        self,
        id: UUID,
        update_dto: ProductForRecipeUpdateDto,
        user_id: UUID,
        is_admin=False,
    ) -> RecipeOutputDto:
        try:
            product_for_recipe: ProductForRecipe = (
                await self._product_for_recipe_repository.aget_by_id(
                    id=id, fetch_fields=["product"]
                )
            )
        except DoesNotExist:
            raise ProductForRecipeNotFound(message=f"Product with id {id} not found.")

        recipe: Recipe = await self._recipe_repository.aget_by_id(
            product_for_recipe.recipe_id
        )
        if recipe.user_id != user_id and not is_admin:
            raise ProductForRecipeNotRecordOwner(
                message=f"User with id {user_id} is not Recipe owner"
            )

        product_for_recipe.update_weight(
            recipe=recipe, weight=update_dto.weight_in_grams
        )

        await self._product_for_recipe_repository.aupdate(product_for_recipe)
        await self._recipe_repository.aupdate(recipe)

        recipe = await self._recipe_repository.aget_by_id(
            id=recipe.id,
            fetch_fields=["products_for_recipe", "products_for_recipe__product"],
        )

        return RecipeOutputDto(
            **self._recipe_repository.convert_snapshot(snapshot=recipe.snapshot)
        )

    async def delete_product(self, id: UUID, user_id: UUID, is_admin=False) -> None:
        try:
            product_for_recipe: ProductForRecipe = (
                await self._product_for_recipe_repository.aget_by_id(id)
            )
        except DoesNotExist:
            raise ProductForRecipeNotFound(message=f"Product with id {id} not found.")

        recipe: Recipe = await self._recipe_repository.aget_by_id(
            product_for_recipe.recipe_id
        )

        if recipe.user_id != user_id and not is_admin:
            raise ProductForRecipeNotRecordOwner(
                message=f"User with id {user_id} is not Recipe owner"
            )

        recipe.delete_product(product_for_recipe)

        await self._product_for_recipe_repository.adelete(product_for_recipe)
        await self._recipe_repository.aupdate(recipe)
