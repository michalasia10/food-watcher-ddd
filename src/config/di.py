from dependency_injector import containers, providers

from src.config.config import ApiConfig
from src.modules.auth.di import AuthContainer
from src.modules.product.di import ProductContainer, ConsumptionContainer
from src.modules.recipe.di import RecipeContainer


class AppContainer(containers.DeclarativeContainer):
    container_config = providers.Configuration()
    raw_api_config = ApiConfig()
    container_config.from_dict(raw_api_config.model_dump())

    api_config = providers.Singleton(ApiConfig)

    #### AUTH / USER ###
    auth = providers.Container(
        AuthContainer,
        container_config=container_config,
        api_config=api_config,
    )

    #### PRODUCT ###
    product = providers.Container(
        ProductContainer,
        container_config=container_config,
        api_config=raw_api_config,
    )

    ### CONSUMPTION ###
    consumption = providers.Container(
        ConsumptionContainer,
        container_config=container_config,
        api_config=api_config,
    )

    ### RECIPE ###
    recipe = providers.Container(
        RecipeContainer,
        container_config=container_config,
        api_config=raw_api_config,
        product_service=product.service,
    )
