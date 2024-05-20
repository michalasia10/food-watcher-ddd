from dependency_injector import containers, providers

from src.modules.product_new.application.service.product import ProductCrudService
from src.modules.product_new.infra.repo.product import ProductTortoiseRepo


class ProductContainer(containers.DeclarativeContainer):
    container_config = providers.Configuration()
    api_config = providers.ItemGetter()

    product_service = providers.Factory(
        ProductCrudService,
        repository=ProductTortoiseRepo,
    )
