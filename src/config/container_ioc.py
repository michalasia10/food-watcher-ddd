from dependency_injector import containers, providers
from sqlalchemy import create_engine

from src.config.api_config import ApiConfig
from src.foundation.infra.db import Base
from src.modules.auth.infra.repository.user import SqlUserRepository
from src.modules.auth.infra.services.authentication import AuthenticationService
from src.modules.auth.infra.usecases.command.user import UserCommand
from src.modules.auth.infra.usecases.query.user import UserQuery
from src.modules.chat.infra.repository.messages import (
    SqlChannelRepository,
    SqlMessageRepository,
    SqlMessageCompositeRepository
)
from src.modules.chat.infra.usecases.command.channel import ChannelCommand
from src.modules.chat.infra.usecases.query.channel import ChannelQuery
from src.modules.products.infra.repository.product import (
    SqlProductRepository,
    SqlDailyUserConsumptionRepository,
    SqlDailyUserProductRepository,
)
from src.modules.products.infra.usecases.add_meal import AddMealI
from src.modules.products.infra.usecases.command.product import ProductCommand
from src.modules.products.infra.usecases.query.product import ProductQuery, UserDayQuery
from src.modules.recipes.infra.repository.recipe import SqlRecipeRepository, SqlRecipeProductRepository
from src.modules.recipes.infra.usecases.command.recipe import RecipeCommand, RecipeProductCommand
from src.modules.recipes.infra.usecases.query.recipe import RecipeQuery


def create_configured_engine(config: ApiConfig | dict, test: bool = False):
    config = config.dict() if isinstance(config, ApiConfig) else config
    base_url: str = config.get("TEST_DATABASE_URL") if test else config.get("DATABASE_URL")
    _base_url = base_url.replace("postgres://", "postgresql://")
    engine = create_engine(
        _base_url, echo=config["DEBUG"]
    )
    Base.metadata.bind = engine
    return engine


def create_request_context(engine):
    from src.foundation.infra.request_context import request_context

    request_context.setup(engine)
    return request_context


class Container(containers.DeclarativeContainer):
    from src.foundation.infra.request_context import RequestContext

    __self__ = providers.Self()
    ### Config ###

    config = providers.Configuration()
    engine = providers.Singleton(create_configured_engine, config)
    api_config = ApiConfig()
    rabitmq_url = providers.Object(api_config.RABBITMQ_URL)

    ### Request Context ###

    request_context: RequestContext = providers.Factory(
        create_request_context, engine=engine
    )

    correlation_id = providers.Factory(
        lambda request_context: request_context.correlation_id.get(), request_context
    )

    ### User ###

    user_repository = providers.Factory(
        SqlUserRepository, db_session=request_context.provided.db_session
    )

    auth_service = providers.Factory(AuthenticationService,
                                     user_repository=user_repository,
                                     secret_key=api_config.SECRET_KEY,
                                     algorithm=api_config.ALGORITHM)

    user_command = providers.Factory(UserCommand, repository=user_repository)
    user_query = providers.Factory(UserQuery, repository=user_repository)

    ### Chat ###

    message_repository = providers.Factory(
        SqlMessageRepository, db_session=request_context.provided.db_session
    )
    channel_repository = providers.Factory(
        SqlChannelRepository, db_session=request_context.provided.db_session
    )
    chanel_query = providers.Factory(ChannelQuery, repository=channel_repository)
    chanel_command = providers.Factory(ChannelCommand, repository=channel_repository)

    composite_message_repository = providers.Factory(
        SqlMessageCompositeRepository,
        message_repository=message_repository,
        channel_repository=channel_repository
    )

    ### Recipes ###
    product_repository = providers.Factory(
        SqlProductRepository, db_session=request_context.provided.db_session
    )


    recipe_repository = providers.Factory(
        SqlRecipeRepository, db_session=request_context.provided.db_session
    )
    recipe_product_repository = providers.Factory(
        SqlRecipeProductRepository, db_session=request_context.provided.db_session
    )
    recipe_query = providers.Factory(RecipeQuery, repository=recipe_repository)
    recipe_command = providers.Factory(RecipeCommand,
                                       repository=recipe_repository,
                                       recipe_product_repository=recipe_product_repository,
                                       product_repository=product_repository)

    recipe_product_command = providers.Factory(RecipeProductCommand,
                                               repository=recipe_product_repository,
                                               )
    recipe_product_query = NotImplementedError

    ### Product ###


    product_query = providers.Factory(ProductQuery, repository=product_repository, recipe_repo=recipe_repository)
    product_command = providers.Factory(ProductCommand, repository=product_repository)

    ### UserConsumption ###
    user_consumption_repository = providers.Factory(
        SqlDailyUserConsumptionRepository, db_session=request_context.provided.db_session
    )

    user_product_repository = providers.Factory(
        SqlDailyUserProductRepository, db_session=request_context.provided.db_session
    )

    user_day_query = providers.Factory(UserDayQuery, repository=user_consumption_repository)
    add_meal_use_case = providers.Factory(AddMealI,
                                          product_repository=product_repository,
                                          daily_product_repository=user_product_repository,
                                          daily_user_consumption_repository=user_consumption_repository)
