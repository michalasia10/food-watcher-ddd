from dependency_injector import containers, providers
from sqlalchemy import create_engine

from .api_config import ApiConfig
from src.foundation.infrastructure.db import Base

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

    request_context: RequestContext = providers.Factory(
        create_request_context, engine=engine
    )

    correlation_id = providers.Factory(
        lambda request_context: request_context.correlation_id.get(), request_context
    )


