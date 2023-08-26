from pydantic import BaseSettings, Field


class ApiConfig(BaseSettings):
    APP_NAME: str = "Food Watcher"
    DEBUG: bool = Field(env="DEBUG", default=True)
    DATABASE_URL: str = Field(
        env="DATABASE_URL",
        default="postgresql://postgres:password@localhost:5432/postgres",
    )
    TEST_DATABASE_URL: str = Field(env="TEST_DATABASE_URL",
                                   default="postgresql://postgres:password@localhost:5433/postgres")
    LOGGER_NAME = "api"
    SECRET_KEY = Field(env="SECRET_KEY", default='ss')
    ALGORITHM = Field(env="ALGORITHM", default="HS256")
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    RELOAD: bool = Field(env="RELOAD", default=False)
    REDIS_URL: str = Field(env="REDIS_URL", default="redis://localhost")
    RABBITMQ_URL: str = Field(env="RABBITMQ_URL", default="amqp://michu:michu@localhost:5672//")


settings = ApiConfig()