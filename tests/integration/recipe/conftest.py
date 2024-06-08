import pytest
import pytest_asyncio

from src.modules.product_new.application.service.product import ProductCrudService
from src.modules.product_new.domain.entity.product import Product
from src.modules.product_new.infra.repo.product import ProductTortoiseRepo
from src.modules.recipe_new.application.service import RecipeService
from src.modules.recipe_new.domain.entity.recipe import Recipe
from src.modules.recipe_new.domain.entity.recipe_product import ProductForRecipe
from src.modules.recipe_new.infra.repo.recipe import RecipeTortoiseRepo
from src.modules.recipe_new.infra.repo.recipe_product import RecipeForProductTortoiseRepo


@pytest.fixture
def recipe_service():
    return RecipeService(
        recipe_repository=RecipeTortoiseRepo,
        product_for_recipe_repository=RecipeForProductTortoiseRepo,
        product_service=ProductCrudService(
            repository=ProductTortoiseRepo
        )
    )


@pytest_asyncio.fixture(scope="function")
async def recipe_record(user_record):
    recipe = Recipe.create(
        name="name",
        description="description",
        link="link",
        user_id=user_record.id
    )
    return await RecipeTortoiseRepo.asave(entity=recipe)


@pytest_asyncio.fixture(scope="function")
async def product_record():
    product = Product.create(
        code=2,
        name='SOME_NAME',
        quantity='SOME_QUANTITY',
        brand='SOME_BRAND',
        size='SOME_SIZE',
        groups='SOME_GROUPS',
        category='SOME_CATEGORY',
        energy_kcal_100g=100.0,
        fat_100g=10.0,
        carbohydrates_100g=20.0,
        sugars_100g=30.0,
        proteins_100g=40.0
    )
    return await ProductTortoiseRepo.asave(entity=product)


@pytest_asyncio.fixture(scope="function")
async def product_record2():
    product = Product.create(
        code=3,
        name='SOME_NAME_2',
        quantity='SOME_QUANTITY_2',
        brand='SOME_BRAND_2',
        size='SOME_SIZE_2',
        groups='SOME_GROUPS_2',
        category='SOME_CATEGORY_2',
        energy_kcal_100g=55.55,
        fat_100g=22.22,
        carbohydrates_100g=33.44,
        sugars_100g=55.0,
        proteins_100g=40.0
    )
    return await ProductTortoiseRepo.asave(entity=product)


@pytest_asyncio.fixture(scope="function")
async def recipe_record_with_products(user_record, product_record2):
    recipe = Recipe.create(
        name="name",
        description="description",
        link="link",
        user_id=user_record.id
    )
    await RecipeTortoiseRepo.asave(entity=recipe)
    product_for_recipe = ProductForRecipe.create(
        recipe=recipe,
        product=product_record2,
        weight_in_grams=255.55
    )
    await RecipeForProductTortoiseRepo.asave(entity=product_for_recipe)
    await RecipeTortoiseRepo.aupdate(entity=recipe)

    product_for_recipe.product = product_record2
    recipe.products_for_recipe = [product_for_recipe]
    return recipe
