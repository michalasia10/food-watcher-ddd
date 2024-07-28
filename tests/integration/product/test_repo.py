import pytest

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


### PRODUCT ###


@pytest.mark.asyncio
async def test_create_and_get_product():
    # given
    product_to_create = Product.create(
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
    await ProductTortoiseRepo.asave(entity=product_to_create)

    # when
    product_get_from_db = await ProductTortoiseRepo.aget_first_from_filter(
        code=product_to_create.code
    )

    # then
    assert product_get_from_db
    assert product_get_from_db.code == product_to_create.code
    assert product_get_from_db.name == product_to_create.name
    assert product_get_from_db.quantity == product_to_create.quantity
    assert product_get_from_db.brand == product_to_create.brand
    assert product_get_from_db.size == product_to_create.size
    assert product_get_from_db.groups == product_to_create.groups
    assert product_get_from_db.category == product_to_create.category
    assert product_get_from_db.energy_kcal_100g == product_to_create.energy_kcal_100g
    assert product_get_from_db.fat_100g == product_to_create.fat_100g
    assert (
        product_get_from_db.carbohydrates_100g == product_to_create.carbohydrates_100g
    )
    assert product_get_from_db.sugars_100g == product_to_create.sugars_100g
    assert product_get_from_db.proteins_100g == product_to_create.proteins_100g
    assert product_get_from_db.updated_at is not None
    assert product_get_from_db.created_at is not None


@pytest.mark.asyncio
async def test_create_multiple_and_get_all_products():
    # given
    num_of_products_to_create = 10
    products_to_create = [
        Product.create(
            code=i,
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
        for i in range(num_of_products_to_create)
    ]
    for product in products_to_create:
        await ProductTortoiseRepo.asave(entity=product)

    # when
    products_get_from_db = await ProductTortoiseRepo.aget_all()

    # then
    assert len(products_get_from_db) == num_of_products_to_create
    allowed_codes = set(range(num_of_products_to_create))

    for product in products_get_from_db:
        assert product.code in allowed_codes


@pytest.mark.asyncio
async def test_update_product():
    # given
    product_to_create = Product.create(
        code=3,
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
    await ProductTortoiseRepo.asave(entity=product_to_create)

    # when
    product_to_create.name = "NEW_NAME"
    await ProductTortoiseRepo.aupdate(entity=product_to_create)

    # then
    product_get_from_db = await ProductTortoiseRepo.aget_first_from_filter(
        code=product_to_create.code
    )
    assert product_get_from_db.name == "NEW_NAME"


@pytest.mark.asyncio
async def test_delete_product():
    # given
    product_to_create = Product.create(
        code=4,
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
    await ProductTortoiseRepo.asave(entity=product_to_create)

    # when
    await ProductTortoiseRepo.adelete(entity=product_to_create)

    # then
    product_get_from_db = await ProductTortoiseRepo.aget_first_from_filter(
        code=product_to_create.code
    )
    assert product_get_from_db is None


### DAILY USER CONSUMPTION ###


@pytest.mark.asyncio
async def test_create_and_get_daily_consumption(user_record):
    # given

    daily_consumption = DailyUserConsumption.create(
        user_id=user_record.id,
    )
    await DailyUserConsumptionTortoiseRepo.asave(entity=daily_consumption)

    # when
    daily_consumption_get_from_db = (
        await DailyUserConsumptionTortoiseRepo.aget_first_from_filter(
            user_id=daily_consumption.user_id
        )
    )

    # then

    assert daily_consumption_get_from_db
    assert daily_consumption_get_from_db.user_id == daily_consumption.user_id
    assert daily_consumption_get_from_db.updated_at is not None
    assert daily_consumption_get_from_db.created_at is not None
    assert daily_consumption_get_from_db.summary_proteins == 0.0
    assert daily_consumption_get_from_db.summary_fats == 0.0
    assert daily_consumption_get_from_db.summary_carbohydrates == 0.0
    assert daily_consumption_get_from_db.summary_calories == 0.0


@pytest.mark.asyncio
async def test_update_daily_consumption(user_record):
    # given
    daily_consumption = DailyUserConsumption.create(
        user_id=user_record.id,
    )
    await DailyUserConsumptionTortoiseRepo.asave(entity=daily_consumption)

    # when
    daily_consumption.summary_proteins = 10.0
    await DailyUserConsumptionTortoiseRepo.aupdate(entity=daily_consumption)

    # then
    daily_consumption_get_from_db = (
        await DailyUserConsumptionTortoiseRepo.aget_first_from_filter(
            user_id=daily_consumption.user_id
        )
    )
    assert daily_consumption_get_from_db.summary_proteins == 10.0


@pytest.mark.asyncio
async def test_delete_daily_consumption(user_record):
    # given
    daily_consumption = DailyUserConsumption.create(
        user_id=user_record.id,
    )
    await DailyUserConsumptionTortoiseRepo.asave(entity=daily_consumption)

    # when
    await DailyUserConsumptionTortoiseRepo.adelete(entity=daily_consumption)

    # then
    daily_consumption_get_from_db = (
        await DailyUserConsumptionTortoiseRepo.aget_first_from_filter(
            user_id=daily_consumption.user_id
        )
    )
    assert daily_consumption_get_from_db is None


### DAILY PRODUCT ###


@pytest.mark.asyncio
async def test_create_and_get_daily_product(user_record):
    # given
    product = Product.create(
        code=3,
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
    await ProductTortoiseRepo.asave(entity=product)

    daily_user_consumption = DailyUserConsumption.create(
        user_id=user_record.id,
    )
    await DailyUserConsumptionTortoiseRepo.asave(entity=daily_user_consumption)

    daily_product = DailyUserProduct.create(
        product=product,
        day=daily_user_consumption,
        weight_in_grams=100.0,
    )

    await DailyUserProductTortoiseRepo.asave(entity=daily_product)

    # when
    daily_product_get_from_db = await DailyUserProductTortoiseRepo.aget_by_id(
        id=daily_product.id
    )

    # then
    assert daily_product_get_from_db
    assert daily_product_get_from_db.product_id == product.id
    assert daily_product_get_from_db.day_id == daily_user_consumption.id
