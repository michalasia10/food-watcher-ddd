from dependency_injector import containers, providers
from sqlalchemy import create_engine

from src.foundation.infrastructure.db import Base
from src.modules.auth.infra.repository.user import SqlUserRepository
from src.modules.auth.infra.services.authentication import AuthenticationService
from src.modules.auth.infra.usecases.command.user import UserCommand
from src.modules.auth.infra.usecases.query.user import UserQuery
from src.modules.products.infra.repository.product import SqlProductRepository
from src.modules.products.infra.usecases.query.product import ProductQuery
from .api_config import ApiConfig


def create_configured_engine(config: ApiConfig | dict):
    config = config.dict() if isinstance(config, ApiConfig) else config
    engine = create_engine(
        config["DATABASE_URL"], echo=config["DEBUG"]
    )
    Base.metadata.bind = engine
    return engine


def create_request_context(engine):
    from foundation.infrastructure.request_context import request_context

    request_context.setup(engine)
    return request_context


class Container(containers.DeclarativeContainer):
    from src.foundation.infrastructure.request_context import RequestContext

    __self__ = providers.Self()
    config = providers.Configuration()
    engine = providers.Singleton(create_configured_engine, config)
    api_config = ApiConfig()

    request_context: RequestContext = providers.Factory(
        create_request_context, engine=engine
    )

    correlation_id = providers.Factory(
        lambda request_context: request_context.correlation_id.get(), request_context
    )
    user_repository = providers.Factory(
        SqlUserRepository, db_session=request_context.provided.db_session
    )
    product_repository = providers.Factory(
        SqlProductRepository, db_session=request_context.provided.db_session
    )

    auth_service = providers.Factory(AuthenticationService,
                                     user_repository=user_repository,
                                     secret_key=api_config.SECRET_KEY,
                                     algorithm=api_config.ALGORITHM)

    user_command = providers.Factory(UserCommand, repository=user_repository)
    user_query = providers.Factory(UserQuery, repository=user_repository)
    product_query = providers.Factory(ProductQuery, repository=product_repository)
