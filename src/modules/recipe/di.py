from dependency_injector import containers, providers

from src.modules.recipe.application.service import RecipeService
from src.modules.recipe.infra.repo.recipe import RecipeTortoiseRepo
from src.modules.recipe.infra.repo.recipe_product import RecipeForProductTortoiseRepo


class RecipeContainer(containers.DeclarativeContainer):
    container_config = providers.Configuration()
    api_config = providers.ItemGetter()
    product_service = providers.Dependency()

    service = providers.Factory(
        RecipeService,
        product_service=product_service,
        product_for_recipe_repository=RecipeForProductTortoiseRepo,
        recipe_repository=RecipeTortoiseRepo,
    )
