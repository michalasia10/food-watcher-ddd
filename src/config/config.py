import sys
from copy import deepcopy

from logfire import loguru_handler, configure
from loguru import logger as loguru_logger
from pydantic import Field
from pydantic_settings import BaseSettings


class ApiConfig(BaseSettings):
    APP_NAME: str = "Food Watcher"
    VERSION: str = "0.1.0"
    DEBUG: bool = Field(
        env="DEBUG",
        default=True
    )
    DATABASE_URL: str = Field(
        env="DATABASE_URL",
        default="postgres://postgres:password@localhost:5432/postgres",
    )
    TEST_DATABASE_URL: str = Field(
        env="TEST_DATABASE_URL",
        default="postgres://postgres:password@localhost:5433/postgres",
    )
    LOGGER_NAME: str = "api"
    SECRET_KEY: str = Field(
        env="SECRET_KEY",
        default="SECRET"
    )
    ALGORITHM: str = Field(
        env="ALGORITHM",
        default="HS256"
    )
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    RELOAD: bool = Field(
        env="RELOAD",
        default=False
    )
    REDIS_URL: str = Field(
        env="REDIS_URL",
        default="redis://localhost"
    )
    RABBITMQ_URL: str = Field(
        env="RABBITMQ_URL",
        default="amqp://michu:michu@localhost:5672//"
    )
    LOGFIRE_TOKEN: str = Field(
        env="LOGFIRE_TOKEN",
        default="token",
    )
    LOGFIRE_APP_NAME: str = Field(
        env="LOGFIRE_APP_NAME",
        default="app_name",
    )

    @property
    def TORTOISE_ORM_CONFIG(self) -> dict:
        return {
            'connections': {
                'default': self.DATABASE_URL,
            },
            'apps': {
                "auth": {
                    'models': [
                        "src.modules.auth.infra.model",
                        "aerich.models",
                    ],
                    "default_connection": "default"
                },
                "product": {
                    'models': [
                        "src.modules.product.infra.model.product",
                        "src.modules.product.infra.model.consumption",
                        "src.modules.product.infra.model.daily_product",
                        "aerich.models",
                    ],
                    "default_connection": "default"
                },
                "recipe": {
                    'models': [
                        "src.modules.recipe.infra.model.recipe",
                        "src.modules.recipe.infra.model.recipe_product",
                        "aerich.models",
                    ],
                    "default_connection": "default"
                },
            },
            'timezone': 'UTC'
        }

    @property
    def TORTOISE_TEST_CONFIG(self) -> dict:
        config = deepcopy(self.TORTOISE_ORM_CONFIG)
        config['connections']['default'] = self.TEST_DATABASE_URL

        return config


settings = ApiConfig()
send_to_logfire = not settings.DEBUG and not 'pytest' in sys.argv[0]
configure(
    send_to_logfire=send_to_logfire,
    token=settings.LOGFIRE_TOKEN if send_to_logfire else None,
    project_name=settings.LOGFIRE_APP_NAME
)
loguru_logger.configure(handlers=[loguru_handler()])
