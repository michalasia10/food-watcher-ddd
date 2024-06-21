from datetime import datetime

from tortoise.exceptions import DoesNotExist
from uuid6 import UUID

from src.core.infra.tortoiserepo import IRepository
from src.modules.product.application.dto.consumption import (
    DailyUserConsumptionOutputDto,
)
from src.modules.product.application.dto.daily_product import DailyUserProductInputDto
from src.modules.product.domain.entity.consumption import DailyUserConsumption
from src.modules.product.domain.entity.daily_product import DailyUserProduct
from src.modules.product.domain.errors import (
    ProductNotFound,
    DailyUserConsumptionNotFound,
    DailyProductNotFound,
    DailyUserConsumptionNotRecordOwner,
)


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
        self, user_id: UUID, skip: int = 0, limit: int = 10
    ) -> list[DailyUserConsumptionOutputDto]:
        """
        Method to get all days of a user with their daily consumption.

        Args:
            user_id: UUID
            skip: int
            limit: int

        Returns: list[DailyUserConsumptionOutputDto]

        """
        days = await self._consumption_repository.aget_all_from_filter(
            user_id=user_id,
            offset=skip,
            limit=limit,
            fetch_fields=["products", "products__product"],
        )

        return [
            DailyUserConsumptionOutputDto(
                **self._consumption_repository.convert_snapshot(snapshot=day.snapshot)
            )
            for day in days
        ]

    async def get_day_by_id(self, day_id: UUID) -> DailyUserConsumptionOutputDto:
        """
        Method to get a day by its id.

        Args:
            day_id: UUID

        Returns: DailyUserConsumptionOutputDto

        """
        try:
            day = await self._consumption_repository.aget_by_id(
                id=day_id,
                fetch_fields=["products", "products__product"],
            )
        except DoesNotExist:
            raise DailyUserConsumptionNotFound(
                f"Daily consumption with id {day_id} not found."
            )

        return DailyUserConsumptionOutputDto(
            **self._consumption_repository.convert_snapshot(snapshot=day.snapshot)
        )

    async def get_day_by_datetime(
        self, date: datetime, user_id: UUID
    ) -> DailyUserConsumptionOutputDto:
        """
        Method to get a day by its datetime.

        Args:
            date: str
            user_id: UUID

        Returns: DailyUserConsumptionOutputDto

        """
        day = await self._consumption_repository.aget_first_from_filter(
            user_id=user_id,
            date=date,
            fetch_fields=["products", "products__product"],
        )
        if day is None:
            raise DailyUserConsumptionNotFound(
                f"Daily consumption with date {date} not found for user {user_id}."
            )

        return DailyUserConsumptionOutputDto(
            **self._consumption_repository.convert_snapshot(snapshot=day.snapshot)
        )

    async def add_meal(
        self, user_id: UUID, input_dto: DailyUserProductInputDto
    ) -> DailyUserConsumptionOutputDto:
        """
        Method to add a meal to the daily consumption of a user.

        Meal will be calculated based on the weight of the product and the macros of the product.
        Daily consumption will be created if it does not exist, otherwise it will be updated
        with recalculated macros / calories.

        Args:
            user_id: UUID
            input_dto: DailyUserProductInputDto

        Returns: DailyUserConsumptionOutputDto

        """

        try:
            product = await self._product_repository.aget_by_id(input_dto.product_id)
        except DoesNotExist:
            raise ProductNotFound(f"Product with id {input_dto.product_id} not found")

        day: DailyUserConsumption = (
            await self._consumption_repository.aget_first_from_filter(
                user_id=user_id,
                date=input_dto.date,
            )
        )

        if day is None:
            entity = DailyUserConsumption.create(user_id=user_id)
            await self._consumption_repository.asave(entity=entity)
            day: DailyUserConsumption = await self._consumption_repository.aget_by_id(
                entity.id
            )

        daily_product = DailyUserProduct.create(
            product=product,
            day=day,
            weight_in_grams=input_dto.weight_in_grams,
            type=input_dto.type,
        )

        await self._daily_product_repository.asave(entity=daily_product)
        await self._consumption_repository.aupdate(entity=day)

        updated_day: DailyUserConsumption = (
            await self._consumption_repository.aget_by_id(
                id=day.id,
                fetch_fields=["products", "products__product"],
            )
        )

        return DailyUserConsumptionOutputDto(
            **self._consumption_repository.convert_snapshot(
                snapshot=updated_day.snapshot
            )
        )

    async def delete_meal(
        self, user_id: UUID, daily_product_id: UUID
    ) -> DailyUserConsumptionOutputDto:
        try:
            product = await self._daily_product_repository.aget_by_id(daily_product_id)
        except DoesNotExist:
            raise DailyProductNotFound(f"Product with id {daily_product_id} not found")

        day: DailyUserConsumption = await self._consumption_repository.aget_by_id(
            id=product.day_id,
        )

        if day.user_id != user_id:
            raise DailyUserConsumptionNotRecordOwner(
                f"Daily consumption with id {day.id} does not belong to user {user_id}."
            )

        day.delete_product(product)
        await self._daily_product_repository.adelete(entity=product)
        await self._consumption_repository.aupdate(entity=day)

        updated_day: DailyUserConsumption = (
            await self._consumption_repository.aget_by_id(
                id=day.id,
                fetch_fields=["products", "products__product"],
            )
        )

        return DailyUserConsumptionOutputDto(
            **self._consumption_repository.convert_snapshot(
                snapshot=updated_day.snapshot
            )
        )
