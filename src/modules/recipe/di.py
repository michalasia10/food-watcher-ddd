from dependency_injector import containers, providers

from src.modules.recipe.application.service import RecipeService
from src.modules.recipe.infra.repo.meilsearch.recipe import RecipeMeiliSearchEngineRepo
from src.modules.recipe.infra.repo.postgres.recipe import RecipeTortoiseRepo
from src.modules.recipe.infra.repo.postgres.recipe_product import (
    RecipeForProductTortoiseRepo,
)


class RecipeContainer(containers.DeclarativeContainer):
    container_config = providers.Configuration()
    api_config = providers.ItemGetter()
    product_service = providers.Dependency()

    service = providers.Factory(
        RecipeService,
        product_service=product_service,
        product_for_recipe_repository=RecipeForProductTortoiseRepo,
        recipe_repository=RecipeTortoiseRepo,
        search_repo=providers.Factory(
            RecipeMeiliSearchEngineRepo,
            meilisearch_url=api_config.MEILISEARCH_URL,
            meilisearch_master_key=api_config.MEILISEARCH_MASTER_KEY,
        ),
    )
