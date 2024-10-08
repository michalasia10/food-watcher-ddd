from typing import Any
from uuid import UUID

import pytest
import pytest_asyncio

from src.modules.product.application.service.consumption import ConsumptionService, IUserSettingsService
from src.modules.product.application.service.product import ProductCrudService
from src.modules.product.domain.entity.consumption import DailyUserConsumption
from src.modules.product.domain.entity.daily_product import DailyUserProduct
from src.modules.product.domain.entity.product import Product
from src.modules.product.infra.repo.postgres.consumption import (
    DailyUserConsumptionTortoiseRepo,
)
from src.modules.product.infra.repo.postgres.daily_product import (
    DailyUserProductTortoiseRepo,
)
from src.modules.product.infra.repo.postgres.product import ProductTortoiseRepo
from tests.integration.conftest import InMemorySearchRepository
from dataclasses import dataclass


@dataclass
class FakeMacro:
    proteins: float | None
    fats: float | None
    carbs: float | None
    calories: float | None

    def model_dump(self):
        return {
            "proteins": self.proteins,
            "fats": self.fats,
            "carbs": self.carbs,
            "calories": self.calories,
        }


@dataclass
class FakeUser:
    macro: FakeMacro


class FakeUserSettingsService(IUserSettingsService):
    async def get_by_user_id(self, user_id: UUID) -> Any:
        return FakeUser(
            macro=FakeMacro(
                proteins=100.0,
                fats=100.0,
                carbs=100.0,
                calories=100.0,
            ),
        )


@pytest.fixture
def consumption_service(secret_key, algorithm):
    return ConsumptionService(
        product_repository=ProductTortoiseRepo,
        daily_product_repository=DailyUserProductTortoiseRepo,
        consumption_repository=DailyUserConsumptionTortoiseRepo,
        settings_service=FakeUserSettingsService(),
    )


@pytest.fixture
def product_service():
    return ProductCrudService(
        repository=ProductTortoiseRepo,
        search_repo=InMemorySearchRepository(),
    )


@pytest_asyncio.fixture(scope="function")
async def product_record():
    product = Product.create(
        code=2,
        name="SOME_NAME",
        quantity="SOME_QUANTITY",
        brand="SOME_BRAND",
        size="SOME_SIZE",
        groups="SOME_GROUPS",
        category="SOME_CATEGORY",
        energy_kcal_100g=100.0,
        fat_100g=10.0,
        carbohydrates_100g=20.0,
        sugars_100g=30.0,
        proteins_100g=40.0,
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
