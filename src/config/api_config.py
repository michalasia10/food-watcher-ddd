from copy import deepcopy
from typing import Type

from pydantic import Field
from pydantic_settings import BaseSettings


class Router:
    def db_for_read(self, model):
        return "default"

    def db_for_write(self, model):
        return "default"


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

    @property
    def TORTOISE_ORM_CONFIG(self) -> dict:
        return {
            "routers": ["src.config.api_config.Router"],
            'connections': {
                'default': self.DATABASE_URL,
            },
            'apps': {
                "auth": {
                    'models': [
                        "src.modules.auth_new.infra.model",
                        "aerich.models",
                    ],
                    "default_connection": "default"
                },
                "product": {
                    'models': [
                        "src.modules.product_new.infra.model.product",
                        "src.modules.product_new.infra.model.consumption",
                        # "src.modules.product_new.infra.model.daily_product",
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
