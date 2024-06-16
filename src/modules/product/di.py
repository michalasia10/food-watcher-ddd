from dependency_injector import containers, providers

from src.modules.product.application.service.consumption import ConsumptionService
from src.modules.product.application.service.product import ProductCrudService
from src.modules.product.infra.repo.consumption import DailyUserConsumptionTortoiseRepo
from src.modules.product.infra.repo.daily_product import DailyUserProductTortoiseRepo
from src.modules.product.infra.repo.product import ProductTortoiseRepo


class ProductContainer(containers.DeclarativeContainer):
    container_config = providers.Configuration()
    api_config = providers.ItemGetter()

    service = providers.Factory(
        ProductCrudService,
        repository=ProductTortoiseRepo,
    )


class ConsumptionContainer(containers.DeclarativeContainer):
    container_config = providers.Configuration()
    api_config = providers.ItemGetter()

    service = providers.Factory(
        ConsumptionService,
        product_repository=ProductTortoiseRepo,
        daily_product_repository=DailyUserProductTortoiseRepo,
        consumption_repository=DailyUserConsumptionTortoiseRepo,
    )
