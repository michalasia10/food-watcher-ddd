import uvicorn

from src.config.api_config import settings

uvicorn.run(
    "api.main:app", host=settings.HOST, port=settings.PORT, reload=settings.RELOAD
)
