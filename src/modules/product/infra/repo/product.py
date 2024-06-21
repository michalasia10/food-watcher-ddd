from src.core.infra.tortoiserepo import TortoiseRepo
from src.modules.product.domain.entity.product import Product as ProductEntity
from src.modules.product.infra.model.product import Product as ProductModel


class ProductTortoiseRepo(TortoiseRepo[ProductModel, ProductEntity]):
    model = ProductModel
    entity = ProductEntity
