from abc import abstractmethod

from src.foundation.application.queries import QueryBase
from src.modules.products.app.usecases.dtos.product import ProductOutputDto


class ProductQuery(QueryBase):

    @abstractmethod
    def get_all(self, skip: int, limit: int) -> list[ProductOutputDto]:
        ...
