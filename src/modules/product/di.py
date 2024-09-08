from dependency_injector import containers, providers

from src.modules.product.application.service.consumption import ConsumptionService
from src.modules.product.application.service.product import ProductCrudService
from src.modules.product.infra.repo.meilsearch.product import (
    ProductMeiliSearchEngineRepo,
)
from src.modules.product.infra.repo.postgres.consumption import (
    DailyUserConsumptionTortoiseRepo,
)
from src.modules.product.infra.repo.postgres.daily_product import (
    DailyUserProductTortoiseRepo,
)
from src.modules.product.infra.repo.postgres.product import ProductTortoiseRepo


class ProductContainer(containers.DeclarativeContainer):
    container_config = providers.Configuration()
    api_config = providers.ItemGetter()

    service = providers.Factory(
        ProductCrudService,
        repository=ProductTortoiseRepo,
        search_repo=providers.Factory(
            ProductMeiliSearchEngineRepo,
            meilisearch_url=api_config.MEILISEARCH_URL,
            meilisearch_master_key=api_config.MEILISEARCH_MASTER_KEY,
        ),
    )


class ConsumptionContainer(containers.DeclarativeContainer):
    container_config = providers.Configuration()
    api_config = providers.ItemGetter()
    settings_service = providers.Dependency()

    service = providers.Factory(
        ConsumptionService,
        product_repository=ProductTortoiseRepo,
        daily_product_repository=DailyUserProductTortoiseRepo,
        consumption_repository=DailyUserConsumptionTortoiseRepo,
        settings_service=settings_service,
    )
