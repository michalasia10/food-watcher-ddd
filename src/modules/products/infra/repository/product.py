from typing import Any, NoReturn

from modules.products.app.repository.product import ProductRepository
from modules.products.domain.value_objects import ProductID
from src.foundation.infrastructure.repository import Repository
from src.modules.products.domain.entities import Product
from src.modules.products.infra.models.product import Product as ProductModel


class SqlProductRepository(Repository, ProductRepository):
    model = ProductModel

    def get_by_id(self, id: ProductID) -> Product:
        return self.session.query(self.model).filter_by(id=str(id)).first()

    def create(self, entity: Product) -> NoReturn:
        raise NotImplementedError

    def update(self, entity: Product):
        raise NotImplementedError

    def get_by_field_value(self, field: str, value: Any) -> Product:
        data = self.session.query(self.model).filter_by(**{field: value}).first()
        return self.data_to_entity(data, Product)

    def delete(self, id: Product) -> NoReturn:
        raise NotImplementedError

    def exists(self, field: str, value: Any) -> bool:
        return bool(self.session.query(self.model).filter_by(**{field: value}).first())

    def get_all(self) -> list[Product]:
        data = self.session.query(self.model).all()
        return [self.data_to_entity(dat, Product) for dat in data]

    def get_all_pagination(self, skip: int, limit: int) -> list[Product]:
        data = self.session.query(self.model).offset(skip).limit(limit).all()
        return [self.data_to_entity(dat, Product) for dat in data]
