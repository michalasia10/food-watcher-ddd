from src.foundation.domain.value_objects import UUID
from src.modules.products.app.repository.product import ProductRepository, DailyUserConsumptionRepository
from src.modules.products.app.usecases.dtos.product import ProductOutputDto, DailyUserConsumptionOutputDto
from src.modules.products.app.usecases.query.product import (
    ProductQuery as ProductQueryBase,
    UserDayQuery as UserDayQueryBase
)
from src.modules.products.domain.exceptions import UserDayNotFound
from src.modules.products.domain.value_objects import ProductID, DailyUserConsID


class ProductQuery(ProductQueryBase):
    def __init__(self, repository: ProductRepository):
        self._repository = repository

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ProductOutputDto]:
        return [ProductOutputDto(**product.to_dict()) for product in self._repository.get_all_pagination(skip, limit)]

    def get_by_id(self, id: UUID) -> ProductOutputDto:
        user = self._repository.get_by_id(ProductID(id))
        return ProductOutputDto(**user.to_dict())


class UserDayQuery(UserDayQueryBase):
    def __init__(self, repository: DailyUserConsumptionRepository):
        self._repository = repository

    def get_all_user_days(self, user_id: str, skip: int, limit: int) -> list[DailyUserConsumptionOutputDto]:
        return [DailyUserConsumptionOutputDto(**day.to_dict()) for day in
                self._repository.get_all_pagination(skip, limit, user_id=user_id) if day]

    def get_day_by_id(self, id: DailyUserConsID) -> DailyUserConsumptionOutputDto:
        day = self._repository.get_by_id(id)
        if day:
            return DailyUserConsumptionOutputDto(**day.to_dict()) if day else {}
        else:
            raise UserDayNotFound("User's day not found")

    def get_day_by_datetime(self, datetime: str, user_id: str) -> DailyUserConsumptionOutputDto:
        day = self._repository.get_by_field_values(raw=False, date=datetime, user_id=user_id)

        if day:
            return DailyUserConsumptionOutputDto(**day.to_dict())
        else:
            raise UserDayNotFound("User's day not found")
