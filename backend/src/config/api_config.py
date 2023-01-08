from pydantic import BaseSettings, Field


class ApiConfig(BaseSettings):
    APP_NAME: str = "Food Watcher"
    DEBUG: bool = Field(env="DEBUG", default=True)
    DATABASE_URL: str = Field(
        env="DATABASE_URL",
        default="postgresql://postgres:password@localhost:5432/postgres",
    )
    LOGGER_NAME = "api"
    SECRET_KEY = Field(env="SECRET_KEY",default='ss')
    ALGORITHM = Field(env="ALGORITHM",default="HS256")