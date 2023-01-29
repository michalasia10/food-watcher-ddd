from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from api.shared import dependency, bearer_auth
from config.container_ioc import Container
from modules.products.app.usecases import ProductQuery, ProductOutputDto

router = APIRouter(tags=['products'])


@router.get('/products/')
@inject
def product(user: HTTPBearer = Depends(bearer_auth),
            query: ProductQuery = dependency(Container.product_query),
            skip: int = 0,
            limit: int = 100
            ) -> list[ProductOutputDto]:
    return query.get_all(skip, limit)
