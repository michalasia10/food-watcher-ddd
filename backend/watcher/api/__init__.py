import uvicorn
from fastapi import FastAPI

from watcher.api import main
from watcher.main.container_ioc import Container


def create_app() -> FastAPI:
    container = Container()
    # db = container.db()
    # db.create_database()

    app = FastAPI()
    app.include_router(api.app)
    app.container = Container()
    # s = Container()
    # s.init_resources()
    # s.wire(modules=[api])

    return app



if __name__ == '__main__':
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=5000)
