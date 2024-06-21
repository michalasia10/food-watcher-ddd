from typing import Any

from modules.products.app.repository.product import ProductRepository
from src.modules.recipes.app.repository.recipe import RecipeRepository, ProductRecipeRepository
from src.modules.recipes.app.usecases.command.recipe import (
    RecipeCommand as RecipeCommandBase,
    RecipeProductCommand as RecipeProductCommandBase
)
from src.modules.recipes.app.usecases.dtos.recipe import (
    RecipeInputDto,
    RecipeOutputDto,
    RecipeProductInputDto,
    RecipeProductOutputDto
)
from src.modules.recipes.infra.models.recipe import ProductForRecipe as ProductForRecipeModel
from src.modules.recipes.domain.entities import Recipe as RecipeE, ProductRecipe as ProductRecipeE
from src.modules.recipes.domain.exceptions import RecipeNotFound, RecipeAlreadyExists, RecipeProductNotFound
from src.modules.recipes.domain.value_objects import RecipeID


class RecipeCommand(RecipeCommandBase):

    def __init__(
            self,
            repository: RecipeRepository,
            recipe_product_repository: ProductRecipeRepository,
            product_repository: ProductRepository
    ) -> None:

        self._repository = repository
        self._recipe_product_repository = recipe_product_repository
        self._product_repository = product_repository

    def _create_entities_with_macros(self, recipe: RecipeInputDto) -> tuple[RecipeE, list[tuple[Any, ProductRecipeE]]]:
        recipe_products_e: list[tuple[Any, ProductRecipeE]] = []
        recipe_e = RecipeE(name=recipe.name,
                           description=recipe.description,
                           link=recipe.link
                           )
        product: RecipeProductInputDto
        for product in recipe.products:
            base_product = self._product_repository.get_by_id(product.product_id, raw=True)
            recipe_product_e = ProductRecipeE(weight_in_grams=product.weight_in_grams)
            recipe_product_e.calculate_macros(product=base_product)
            recipe_e.add_product(recipe_product_e)
            recipe_products_e.append((base_product, recipe_product_e))

        return recipe_e, recipe_products_e

    def _create_recipe_in_db(self, recipe_e: RecipeE, recipe_products_e: list[tuple[Any, ProductRecipeE]]):
        recipe_record = self._repository.create(recipe_e, raw=True)
        recipe_product_e: ProductRecipeE
        for recipe_product_e in recipe_products_e:
            base_product, product = recipe_product_e
            values = dict(
                product=base_product,
                weight_in_grams=product.weight_in_grams,
                calories=product.calories,
                proteins=product.proteins,
                fats=product.fats,
                carbohydrates=product.carbohydrates,
            )
            product_recipe = self._recipe_product_repository.get_by_field_values(raw=True, **values)
            if product_recipe is not None:
                recipe_record.products.append(product_recipe)
            else:
                new_recipe_product = ProductForRecipeModel(**values)
                recipe_record.products.append(new_recipe_product)

        self._repository.commit()
        return recipe_record

    def create(self, recipe: RecipeInputDto) -> RecipeOutputDto:
        if self._repository.exists('name', recipe.name):
            raise RecipeAlreadyExists('Recipe already exists.')

        recipe_e, recipe_products_e = self._create_entities_with_macros(recipe)

        recipe_record = self._create_recipe_in_db(recipe_e, recipe_products_e)
        return self._repository.get_by_id(recipe_record.id)

    def delete(self, id: RecipeID):
        if not self._repository.exists('id', id):
            raise RecipeNotFound('Product not found.')
        self._repository.delete(id)

    def update(self, id: RecipeID, recipe: RecipeInputDto) -> RecipeOutputDto:
        raise NotImplementedError


class RecipeProductCommand(RecipeProductCommandBase):

    def __init__(self, repository: ProductRecipeRepository) -> None:
        self._repository = repository

    def create(self, recipe_product: RecipeProductInputDto) -> RecipeProductOutputDto:
        raise NotImplementedError

    def delete(self, id: RecipeID):
        if not self._repository.exists('id', id):
            raise RecipeProductNotFound('Recipe not found.')

        recipe_product = self._repository.get_by_id(id, raw=True)
        recipe = recipe_product.recipe
        recipe.products.remove(recipe_product)
        return

    def update(self, id: RecipeID, recipe_product: RecipeProductInputDto) -> RecipeProductOutputDto:
        if not self._repository.exists('id', id):
            raise RecipeProductNotFound('Recipe not found.')

        recipe_product_record = self._repository.update(id, ProductRecipeE(
            weight_in_grams=recipe_product.weight_in_grams
        ))
        return RecipeProductOutputDto(**recipe_product_record.to_dict())
