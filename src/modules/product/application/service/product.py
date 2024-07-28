from uuid import UUID

from loguru import logger
from tortoise.exceptions import DoesNotExist

from src.core.app.service import BaseCrudService
from src.modules.product.application.dto.product import (
    ProductInputDto,
    ProductOutputDto,
)
from src.modules.product.domain.entity.product import Product
from src.modules.product.domain.errors import ProductNotRecordOwner, ProductNotFound


class ProductCrudService(BaseCrudService):
    OUTPUT_DTO = ProductOutputDto
    NOT_RECORD_OWNER_ERROR = (
        ProductNotRecordOwner,
        "You are not allowed to update product with {id} id.",
    )
    NOT_FOUND_ERROR = (ProductNotFound, "Product not found with {id} id.")
    DOES_NOT_EXIST_ERROR = DoesNotExist

    async def create(
        self, input_dto: ProductInputDto, user_id: UUID = None, **kwargs
    ) -> ProductOutputDto:
        input_as_dict = input_dto.model_dump()
        input_as_dict["user_id"] = user_id

        product = Product.create(**input_as_dict)
        await self._repository.asave(product)

        try:
            await self._search_repo.acreate_document(document=product.snapshot)
        except Exception as e:
            logger.error(f"Error creating document in search index: {e}")

        return ProductOutputDto(**product.snapshot)
