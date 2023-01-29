from abc import ABC, abstractmethod

from src.modules.products.app.usecases.dtos.product import ProductOutputDto


class ProductQuery(ABC):

    @abstractmethod
    def get_all(self, skip: int, limit: int) -> list[ProductOutputDto]:
        ...
