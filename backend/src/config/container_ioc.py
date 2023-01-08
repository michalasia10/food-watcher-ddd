from dependency_injector import containers, providers
from sqlalchemy import create_engine

from foundation.infrastructure.request_context import RequestContext


def create_configured_engine(config):
    engine = create_engine(
        config["DATABASE_URL"], echo=config["DEBUG"]
    )
    from foundation.infrastructure.database import Base
    Base.metadata.bind = engine
    return engine


def create_request_context(engine):
    from foundation.infrastructure.request_context import request_context

    request_context.setup(engine)
    return request_context


class Container(containers.DeclarativeContainer):
    __self__ = providers.Self()
    config = providers.Configuration()
    engine = providers.Singleton(create_configured_engine, config)

    request_context: RequestContext = providers.Factory(
        create_request_context, engine=engine
    )

    correlation_id = providers.Factory(
        lambda request_context: request_context.correlation_id.get(), request_context
    )
