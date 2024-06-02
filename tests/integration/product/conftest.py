import pytest
import pytest_asyncio

from src.modules.product_new.application.service.consumption import ConsumptionService
from src.modules.product_new.domain.entity.consumption import DailyUserConsumption
from src.modules.product_new.domain.entity.daily_product import DailyUserProduct
from src.modules.product_new.domain.entity.product import Product
from src.modules.product_new.infra.repo.consumption import DailyUserConsumptionTortoiseRepo
from src.modules.product_new.infra.repo.daily_product import DailyUserProductTortoiseRepo
from src.modules.product_new.infra.repo.product import ProductTortoiseRepo


@pytest.fixture
def consumption_service(secret_key, algorithm):
    return ConsumptionService(
        product_repository=ProductTortoiseRepo,
        daily_product_repository=DailyUserProductTortoiseRepo,
        consumption_repository=DailyUserConsumptionTortoiseRepo,
    )


@pytest_asyncio.fixture(scope="function")
async def product_record():
    product = Product.create(
        code=2,
        name='SOME_NAME',
        quantity='SOME_QUANTITY',
        brand='SOME_BRAND',
        size='SOME_SIZE',
        groups='SOME_GROUPS',
        category='SOME_CATEGORY',
        energy_kcal_100g=100.0,
        fat_100g=10.0,
        carbohydrates_100g=20.0,
        sugars_100g=30.0,
        proteins_100g=40.0
    )
    return await ProductTortoiseRepo.asave(entity=product)


@pytest_asyncio.fixture(scope="function")
async def consumption_record(user_record):
    consumption = DailyUserConsumption.create(
        user_id=user_record.id,
    )
    await DailyUserConsumptionTortoiseRepo.asave(entity=consumption)
    return consumption


@pytest_asyncio.fixture(scope="function")
async def consumption_with_product(consumption_record, product_record):
    daily_product = DailyUserProduct.create(
        product=product_record,
        day=consumption_record,
        weight_in_grams=100.0,
    )
    await DailyUserProductTortoiseRepo.asave(entity=daily_product)
    await DailyUserConsumptionTortoiseRepo.aupdate(entity=consumption_record)

    return consumption_record
