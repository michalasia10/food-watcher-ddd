from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from tortoise.exceptions import DoesNotExist
from uuid6 import UUID

from src.core.infra.repo.tortoiserepo import IPostgresRepository
from src.modules.product.application.dto.consumption import (
    DailyUserConsumptionOutputDto,
)
from src.modules.product.application.dto.daily_product import DailyUserProductInputDto
from src.modules.product.domain.entity.consumption import DailyUserConsumption
from src.modules.product.domain.entity.daily_product import DailyUserProduct
from src.modules.product.domain.entity.meal import Meal
from src.modules.product.domain.enum import UserProductType
from src.modules.product.domain.errors import (
    ProductNotFound,
    DailyUserConsumptionNotFound,
    DailyProductNotFound,
    DailyUserConsumptionNotRecordOwner,
)


class IUserSettingsService(ABC):
    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> Any:
        pass


class ConsumptionService:
    """
    Service class for consumption.
    """

    def __init__(
        self,
        product_repository: [IPostgresRepository],
        daily_product_repository: [IPostgresRepository],
        consumption_repository: [IPostgresRepository],
        settings_service: IUserSettingsService,
    ):
        self._consumption_repository: IPostgresRepository = consumption_repository
        self._product_repository: IPostgresRepository = product_repository
        self._daily_product_repository: IPostgresRepository = daily_product_repository
        self._user_settings_service: IUserSettingsService = settings_service

    async def _get_products_and_set_meals(self, day: DailyUserConsumption) -> list[dict]:
        """
        Method to get all products from the daily consumption and set them ( group ) to the meals.

        Args:
            day: DailyUserConsumption

        Returns: list[dict]

        """
        meals = []

        for _type in UserProductType:
            meal = Meal(type=_type.value)
            products = await self._daily_product_repository.aget_all_from_filter(
                day_id=day.id,
                type=_type,
                fetch_fields=["product"],
            )
            meal.add_products(products)
            meals.append(
                dict(
                    meal=meal.type,
                    products=meal.products,
                    summary=dict(
                        proteins=meal.summary_proteins,
                        fats=meal.summary_fats,
                        carbs=meal.summary_carbohydrates,
                        calories=meal.summary_calories,
                    ),
                )
            )
        return meals

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
        )

        for day in days:
            meals = await self._get_products_and_set_meals(day)
            day.meals = meals

        user_settings = await self._user_settings_service.get_by_user_id(user_id=user_id)

        return [
            DailyUserConsumptionOutputDto(
                user=user_settings.macro.model_dump(),
                **self._consumption_repository.convert_snapshot(snapshot=day.snapshot),
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
            )
        except DoesNotExist:
            raise DailyUserConsumptionNotFound(f"Daily consumption with id {day_id} not found.")

        day.meals = await self._get_products_and_set_meals(day)
        user_settings = await self._user_settings_service.get_by_user_id(user_id=day.user_id)

        return DailyUserConsumptionOutputDto(
            user=user_settings.macro.model_dump(),
            **self._consumption_repository.convert_snapshot(snapshot=day.snapshot),
        )

    async def get_day_by_datetime(self, date: datetime, user_id: UUID) -> DailyUserConsumptionOutputDto:
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
        )
        if day is None:
            raise DailyUserConsumptionNotFound(f"Daily consumption with date {date} not found for user {user_id}.")

        day.meals = await self._get_products_and_set_meals(day)
        user_settings = await self._user_settings_service.get_by_user_id(user_id=day.user_id)

        return DailyUserConsumptionOutputDto(
            user=user_settings.macro.model_dump(),
            **self._consumption_repository.convert_snapshot(snapshot=day.snapshot),
        )

    async def add_meal(self, user_id: UUID, input_dto: DailyUserProductInputDto) -> DailyUserConsumptionOutputDto:
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

        day: DailyUserConsumption = await self._consumption_repository.aget_first_from_filter(
            user_id=user_id,
            date=input_dto.date,
        )

        if day is None:
            entity = DailyUserConsumption.create(user_id=user_id, date_value=input_dto.date)
            await self._consumption_repository.asave(entity=entity)
            day: DailyUserConsumption = await self._consumption_repository.aget_by_id(entity.id)

        daily_product = DailyUserProduct.create(
            product=product,
            day=day,
            weight_in_grams=input_dto.weight_in_grams,
            type=input_dto.type,
        )

        await self._daily_product_repository.asave(entity=daily_product)
        await self._consumption_repository.aupdate(entity=day)

        updated_day: DailyUserConsumption = await self._consumption_repository.aget_by_id(
            id=day.id,
        )

        updated_day.meals = await self._get_products_and_set_meals(updated_day)
        user_settings = await self._user_settings_service.get_by_user_id(user_id=user_id)

        return DailyUserConsumptionOutputDto(
            user=user_settings.macro.model_dump(),
            **self._consumption_repository.convert_snapshot(snapshot=updated_day.snapshot),
        )

    async def delete_meal(self, user_id: UUID, daily_product_id: UUID) -> DailyUserConsumptionOutputDto:
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

        updated_day: DailyUserConsumption = await self._consumption_repository.aget_by_id(
            id=day.id,
        )

        updated_day.meals = await self._get_products_and_set_meals(updated_day)
        user_settings = await self._user_settings_service.get_by_user_id(user_id=user_id)

        return DailyUserConsumptionOutputDto(
            user=user_settings.macro.model_dump(),
            **self._consumption_repository.convert_snapshot(snapshot=updated_day.snapshot),
        )
