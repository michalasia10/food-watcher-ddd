from abc import abstractmethod

from foundation.domain.value_objects import UUID
from src.foundation.application.queries import QueryBase
from src.modules.products.app.usecases.dtos.product import ProductOutputDto, DailyUserConsumptionOutputDto


class ProductQuery(QueryBase):

    @abstractmethod
    def get_all(self, skip: int, limit: int) -> list[ProductOutputDto]:
        ...


class UserDayQuery(QueryBase):

    @abstractmethod
    def get_all_user_days(self, user_id: UUID, skip: int, limit: int) -> list[DailyUserConsumptionOutputDto]:
        ...

    @abstractmethod
    def get_day_by_id(self, id: UUID) -> DailyUserConsumptionOutputDto:
        ...

    @abstractmethod
    def get_day_by_datetime(self, datetime: str) -> DailyUserConsumptionOutputDto:
        ...

    def get_all(self, skip: int, limit: int):
        raise NotImplementedError

    def get_by_id(self, id: str):
        raise NotImplementedError
