from datetime import datetime

from modules.products.domain.exceptions import ProductNotFound
from src.modules.products.app.repository.product import (
    ProductRepository,
    DailyUserProductRepository,
    DailyUserConsumptionRepository
)
from src.modules.products.app.usecases.add_meal import AddMeal
from src.modules.products.app.usecases.dtos.product import DailyUserProductInputDto
from src.modules.products.domain.entities import DailyUserProduct, DailyUserConsumption


class AddMealI(AddMeal):
    def __init__(self,
                 product_repository: ProductRepository,
                 daily_product_repository: DailyUserProductRepository,
                 daily_user_consumption_repository: DailyUserConsumptionRepository
                 ) -> None:
        self._product_repository = product_repository
        self._daily_product_repository = daily_product_repository
        self._daily_user_consumption_repository = daily_user_consumption_repository

    @staticmethod
    def _convert_string_to_date(date: str | datetime) -> datetime:
        return datetime.strptime(date, "%Y-%m-%d") if isinstance(date, str) else date

    def execute(self, daily_product_input: DailyUserProductInputDto) -> None:
        product = self._product_repository.get_by_id(daily_product_input.product_id, raw=True)
        if product is None:
            raise ProductNotFound(f"Product with id {daily_product_input.product_id} not found")

        day: DailyUserConsumption = self._daily_user_consumption_repository \
            .get_by_field_value("user_id", daily_product_input.user_id)

        if day is None:
            record = DailyUserConsumption(user_id=daily_product_input.user_id,
                                          date=self._convert_string_to_date(daily_product_input.date))
            day: DailyUserConsumption = self._daily_user_consumption_repository.create(record)

        daily_product_dto = DailyUserProduct(day_id=day.id,
                                             type=daily_product_input.type,
                                             weight_in_grams=daily_product_input.weight_in_grams)
        daily_product_dto.calculate_macros(product)
        daily_product = self._daily_product_repository.create(daily_product_dto, raw=True)
        product.daily_user_products.append(daily_product)
        day.add_product(daily_product_dto)
        day.products = []

        return self._daily_user_consumption_repository.update(day)
