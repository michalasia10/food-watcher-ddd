from dependency_injector.wiring import inject
from fastapi import APIRouter, HTTPException, Response
from starlette import status

from modules.products.app.usecases.add_meal import AddMeal
from src.api.shared import dependency
from config.container_ioc import Container
from src.foundation.domain.value_objects import UUID
from src.modules.products.app.usecases.dtos.product import DailyUserConsumptionOutputDto, DailyUserProductInputDto
from src.modules.products.app.usecases.query.product import UserDayQuery

router = APIRouter(prefix='/consumption', tags=['consumption'])


@router.get('/{user_id}')
@inject
def get_user_all_days(
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        query: UserDayQuery = dependency(Container.user_day_query)
) -> list[DailyUserConsumptionOutputDto]:
    try:
        return query.get_all_user_days(user_id=user_id, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)


@router.get('/{day_id}')
@inject
def get_day_by_id(
        day_id: UUID,
        query: UserDayQuery = dependency(Container.user_day_query)
) -> DailyUserConsumptionOutputDto:
    try:
        return query.get_day_by_id(day_id)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)


@router.get('/{datetime}')
@inject
def get_day_by_datetime(
        datetime: str,
        query: UserDayQuery = dependency(Container.user_day_query)
) -> DailyUserConsumptionOutputDto:
    try:
        return query.get_day_by_datetime(datetime)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)


@router.post('/')
@inject
def add_meal(
        dto: DailyUserProductInputDto,
        command: AddMeal = dependency(Container.add_meal_use_case)
):
    try:
        command.execute(dto)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)

    return Response(status_code=status.HTTP_201_CREATED)
