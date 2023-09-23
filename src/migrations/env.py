import os
import sys

from alembic import context

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)

from src.config.api_config import ApiConfig
from src.config.container_ioc import create_configured_engine
from src.foundation.infra.db import Base
from src.modules.auth.infra.models.user import User
from src.modules.products.infra.models.product import Product, DailyUserConsumption, DailyUserProducts
from src.modules.chat.infra.models.messages import Message, Channel
from src.modules.recipes.infra.models.recipe import Recipe, ProductForRecipe

config = context.config

target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    config = ApiConfig()
    base_url: str = config.DATABASE_URL
    _base_url = base_url.replace("postgres://", "postgresql://")
    context.configure(
        url=_base_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    config = ApiConfig()
    import sys
    _test = any('pytest' in arg for arg in sys.argv)
    engine = create_configured_engine(config, _test)
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
