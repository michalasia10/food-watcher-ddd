from datetime import datetime
from http import HTTPStatus

from dependency_injector.wiring import inject
from fastapi import APIRouter, Response, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from uuid6 import UUID

from core_new.app.service import IAuthService
from src.api.shared import dependency
from src.config.di import AppContainer
from src.modules.product_new.application.dto.consumption import DailyUserConsumptionOutputDto
from src.modules.product_new.application.dto.daily_product import DailyUserProductInputDto
from src.modules.product_new.application.service.consumption import ConsumptionService

router = APIRouter(
    prefix="/consumption",
    tags=["consumption"]
)


@router.get("/by_user_id/")
@inject
async def get_user_all_days(
        skip: int = 0,
        limit: int = 100,
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
        service: ConsumptionService = dependency(AppContainer.consumption.service),
        auth_service: IAuthService = dependency(AppContainer.auth.auth_service),
) -> list[DailyUserConsumptionOutputDto]:
    """
    Get all days for a user.

    Day is a list of products consumed by a user on a specific day.

    """

    user = await auth_service.verify(token.credentials)

    return await service.get_all_user_days(user_id=user.id, skip=skip, limit=limit)


@router.get("/by_day_id/{day_id}")
@inject
async def get_day_by_id(
        day_id: UUID,
        service: ConsumptionService = dependency(AppContainer.consumption.service)
) -> DailyUserConsumptionOutputDto:
    """
    Get a day by its id.
    """
    return await service.get_day_by_id(day_id=day_id)


@router.get("/by_datetime_for_user/{datetime}/")
@inject
async def get_day_by_datetime(
        datetime: datetime,
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
        service: ConsumptionService = dependency(AppContainer.consumption.service),
        auth_service: IAuthService = dependency(AppContainer.auth.auth_service),
) -> DailyUserConsumptionOutputDto:
    """
    Get a day by its datetime for a user.
    """
    user = await auth_service.verify(token.credentials)

    return await service.get_day_by_datetime(user_id=user.id, datetime=datetime)


@router.post("/")
@inject
async def add_meal(
        dto: DailyUserProductInputDto,
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
        service: ConsumptionService = dependency(AppContainer.consumption.service),
        auth_service: IAuthService = dependency(AppContainer.auth.auth_service),
) -> Response:
    """
    Add a meal for a user's day.

    """

    user = await auth_service.verify(token.credentials)

    await service.add_meal(user_id=user.id, input_dto=dto)

    return Response(status_code=HTTPStatus.CREATED)
