from modules.products.app.repository.product import ProductRepository
from src.modules.recipes.app.repository.recipe import RecipeRepository
from src.modules.recipes.app.usecases.command.recipe import RecipeCommand as RecipeCommandBase
from src.modules.recipes.app.usecases.dtos.recipe import (
    RecipeInputDto,
    RecipeOutputDto,
    ProductRecipeBaseDto
)
from src.modules.recipes.domain.entities import Recipe
from src.modules.recipes.domain.exceptions import RecipeNotFound, RecipeAlreadyExists
from src.modules.recipes.domain.value_objects import RecipeID


class RecipeCommand(RecipeCommandBase):

    def __init__(self, repository: RecipeRepository, product_repository: ProductRepository):
        self._repository = repository
        self._product_repository = product_repository

    def create(self, recipe: RecipeInputDto) -> RecipeOutputDto:
        if self._repository.exists('name', recipe.name):
            raise RecipeAlreadyExists('Recipe already exists.')

        recipe_record = self._repository.create(Recipe(**dict(
            name=recipe.name,
            description=recipe.description,
            link=recipe.link
        )), raw=True)
        product: ProductRecipeBaseDto
        for product in recipe.products:
            product = self._product_repository.get_by_id(product.id, raw=True)
            recipe_record.products.append(product)

        formatted_recipe_record = self._repository.data_to_entity(recipe_record, self._repository.entity)
        return RecipeOutputDto(**formatted_recipe_record.to_dict())

    def delete(self, id: RecipeID):
        if not self._repository.exists('id', id):
            raise RecipeNotFound('Product not found.')
        self._repository.delete(id)

    def update(self, id: RecipeID, recipe: RecipeInputDto) -> RecipeOutputDto:
        raise NotImplementedError
