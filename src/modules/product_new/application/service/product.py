from tortoise.exceptions import DoesNotExist

from modules.product_new.domain.errors import ProductNotRecordOwner, ProductNotFound
from src.core_new.app.service import BaseCrudService
from src.modules.product_new.application.dto.product import ProductInputDto, ProductOutputDto
from src.modules.product_new.domain.entity.product import Product


class ProductCrudService(BaseCrudService):
    OUTPUT_DTO = ProductOutputDto
    NOT_RECORD_OWNER_ERROR = ProductNotRecordOwner("You are not allowed to update this product.")
    NOT_FOUND_ERROR = ProductNotFound("Product not found.")
    DOES_NOT_EXIST_ERROR = DoesNotExist

    async def create(self, input_dto: ProductInputDto) -> ProductOutputDto:
        product = Product.create(
            code=input_dto.code,
            name=input_dto.name,
            quantity=input_dto.quantity,
            brand=input_dto.brand,
            size=input_dto.size,
            groups=input_dto.groups,
            category=input_dto.category,
            energy_kcal_100g=input_dto.energy_kcal_100g,
            fat_100g=input_dto.fat_100g,
            carbohydrates_100g=input_dto.carbohydrates_100g,
            sugars_100g=input_dto.sugars_100g,
            proteins_100g=input_dto.proteins_100g
        )
        await self._repository.asave(product)

        return ProductOutputDto(**product.snapshot)
