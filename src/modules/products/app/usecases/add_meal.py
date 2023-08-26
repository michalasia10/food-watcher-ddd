from abc import ABC, abstractmethod

from modules.auth.domain.value_objects import UserID
from modules.products.app.usecases.dtos.product import DailyUserProductInputDto


class AddMeal(ABC):

    @abstractmethod
    def execute(self, daily_product_input: DailyUserProductInputDto):
        ...
