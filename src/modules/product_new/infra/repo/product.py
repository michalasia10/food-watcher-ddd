from src.core_new.infra.tortoiserepo import TortoiseRepo
from src.modules.product_new.domain.entity.product import Product as ProductEntity
from src.modules.product_new.infra.model.product import Product as ProductModel


class ProductTortoiseRepo(TortoiseRepo[ProductModel, ProductEntity]):
    model = ProductModel
    entity = ProductEntity
