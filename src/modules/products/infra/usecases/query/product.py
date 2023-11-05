from src.foundation.domain.value_objects import UUID
from src.modules.products.app.repository.product import ProductRepository, DailyUserConsumptionRepository
from src.modules.products.app.usecases.dtos.product import ProductOutputDto, DailyUserConsumptionOutputDto
from src.modules.products.app.usecases.query.product import (
    ProductQuery as ProductQueryBase,
    UserDayQuery as UserDayQueryBase
)
from src.modules.products.domain.exceptions import UserDayNotFound
from src.modules.products.domain.value_objects import ProductID, DailyUserConsID
from src.modules.products.domain.entities import Product


class ProductQuery(ProductQueryBase):
    def __init__(
            self,
            repository: ProductRepository,
            recipe_repo
    ):
        self._repository = repository
        self._recipe_repo = recipe_repo

    def _map_to_dto(self, product: Product) -> dict:
        product_dict = product.to_dict()
        product_dict['recipes'] = [self._recipe_repo.get_by_id(product.recipe_id) for product in
                                   product.product_for_recipes]
        del product_dict['product_for_recipes']
        return product_dict

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ProductOutputDto]:
        return [ProductOutputDto(**self._map_to_dto(product)) for product in
                self._repository.get_all_pagination(skip, limit)]

    def get_by_id(self, id: UUID) -> ProductOutputDto:
        product = self._repository.get_by_id(ProductID(id))
        return ProductOutputDto(**self._map_to_dto(product))

    def get_by_name(self, name: str, skip=0, limit=10) -> list[ProductOutputDto]:
        return [ProductOutputDto(**self._map_to_dto(product)) for product in
                self._repository.get_all_by_name(name=name, skip=skip, limit=limit)]


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
