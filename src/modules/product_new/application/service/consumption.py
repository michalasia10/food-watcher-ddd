from datetime import datetime

from uuid6 import UUID

from src.core_new.infra.tortoiserepo import IRepository
from src.modules.product_new.application.dto.consumption import DailyUserConsumptionOutputDto
from src.modules.product_new.application.dto.daily_product import DailyUserProductInputDto
from src.modules.product_new.domain.entity.consumption import DailyUserConsumption
from src.modules.product_new.domain.entity.daily_product import DailyUserProduct
from src.modules.product_new.domain.errors import ProductNotFound, DailyUserConsumptionNotRecordOwner


class ConsumptionService:
    """
    Service class for consumption.
    """

    def __init__(
            self,
            product_repository: [IRepository],
            daily_product_repository: [IRepository],
            consumption_repository: [IRepository],
    ):
        self._consumption_repository: IRepository = consumption_repository
        self._product_repository: IRepository = product_repository
        self._daily_product_repository: IRepository = daily_product_repository

    async def get_all_user_days(
            self,
            user_id: UUID,
            skip: int = 0,
            limit: int = 10
    ) -> list[DailyUserConsumptionOutputDto]:
        """
        Method to get all days of a user with their daily consumption.

        Args:
            user_id: UUID
            skip: int
            limit: int

        Returns: list[DailyUserConsumptionOutputDto]

        """
        return await self._consumption_repository.aget_all_from_filter(user_id=user_id, skip=skip, limit=limit)

    async def get_day_by_id(self, day_id: UUID) -> DailyUserConsumptionOutputDto:
        """
        Method to get a day by its id.

        Args:
            day_id: UUID

        Returns: DailyUserConsumptionOutputDto

        """
        return await self._consumption_repository.aget_by_id(day_id)

    async def get_day_by_datetime(self, datetime: datetime, user_id: UUID) -> DailyUserConsumptionOutputDto:
        """
        Method to get a day by its datetime.

        Args:
            datetime: str
            user_id: UUID

        Returns: DailyUserConsumptionOutputDto

        """
        return await self._consumption_repository.aget_first_from_filter(user_id=user_id, date=datetime)

    async def add_meal(self, user_id: UUID, input_dto: DailyUserProductInputDto) -> DailyUserConsumptionOutputDto:
        """
        Method to add a meal to the daily consumption of a user.

        Meal will be calculated based on the weight of the product and the macros of the product.
        Daily consumption will be created if it does not exist, otherwise it will be updated
        with recalculated macros.

        Args:
            user_id: UUID
            input_dto: DailyUserProductInputDto

        Returns: DailyUserConsumptionOutputDto

        """

        product = await self._product_repository.aget_by_id(input_dto.product_id)
        if product is None:
            raise ProductNotFound(
                f"Product with id {input_dto.product_id} not found"
            )

        day: DailyUserConsumption = await self._consumption_repository.aget_first_from_filter(
            user_id=user_id,
            date=input_dto.date,
        )
        if day is None:
            entity = DailyUserConsumption.create(user_id=user_id)
            await self._consumption_repository.asave(entity=entity)
            day: DailyUserConsumption = await self._consumption_repository.aget_by_id(entity.id)
        elif day.user_id != user_id:
            raise DailyUserConsumptionNotRecordOwner(
                f"User with id {user_id} is not the owner of the day with id {day.id}"
            )

        daily_product = DailyUserProduct.create(
            product=product,
            day=day,
            weight_in_grams=input_dto.weight_in_grams,
            type=input_dto.type,
        )

        await self._daily_product_repository.asave(entity=daily_product)
        await self._consumption_repository.aupdate(entity=day)

        return DailyUserConsumptionOutputDto(**day.snapshot)
