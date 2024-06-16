import uvicorn

from src.config.config import settings

uvicorn.run(
    "src.api.main:app",
    host=settings.HOST,
    port=settings.PORT,
    reload=settings.RELOAD
)
