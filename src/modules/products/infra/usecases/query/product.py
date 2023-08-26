from src.foundation.domain.value_objects import UUID
from src.modules.products.app.repository.product import ProductRepository, DailyUserConsumptionRepository
from src.modules.products.app.usecases.dtos.product import ProductOutputDto, DailyUserConsumptionOutputDto
from src.modules.products.app.usecases.query.product import (
    ProductQuery as ProductQueryBase,
    UserDayQuery as UserDayQueryBase
)
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
                self._repository.get_all_pagination(skip, limit, user_id=user_id)]

    def get_day_by_id(self, id: DailyUserConsID) -> DailyUserConsumptionOutputDto:
        return DailyUserConsumptionOutputDto(**self._repository.get_by_id(id).to_dict())

    def get_day_by_datetime(self, datetime: str) -> DailyUserConsumptionOutputDto:
        return DailyUserConsumptionOutputDto(**self._repository.get_by_field_value("date", datetime).to_dict())
