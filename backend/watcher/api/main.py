from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from watcher.dummy.domain.ports.dummy_ports import ListUser
from watcher.config.container_ioc import Container

app = APIRouter()


@app.get('/all-dummy')
@inject
def get_all(dummy_users: ListUser = Depends(Provide[Container.dummy_users])):
    return dummy_users.all()
