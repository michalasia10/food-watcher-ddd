import datetime

import pytest

from src.modules.auth.domain.value_objects import UserID
from src.modules.products.domain.entities import Product, DailyUserConsumption
from src.modules.products.infra.usecases.add_meal import AddMealI
from src.modules.products.app.usecases.dtos.product import DailyUserProductInputDto

from tests.conftest import base_user_fix, commit_repos, db_session


@pytest.fixture
def product_fix(product_repo):
    product = Product(
        code=28001461,
        name="test",
        quantity="250g",
        brand="Test",
        size="test",
        fat_100g=10.0,
        carbohydrates_100g=10.0,
        sugars_100g=10.0,
        proteins_100g=10.0,
        groups="tests",
        category="tests",
        energy_kcal_100g=10.0
    )
    return product_repo.create(product)


@pytest.fixture
def product_dto_fix(product_fix, base_user_fix):
    return DailyUserProductInputDto(
        product_id=product_fix.id,
        weight_in_grams=100.0,
        date=datetime.datetime.strptime("2021-01-01", "%Y-%m-%d"),
        type=1,
        user_id=UserID(base_user_fix.id),
    )


@pytest.fixture
def add_product_repos(product_repo, daily_user_product_repo, daily_user_consumption_repo):
    return product_repo, daily_user_product_repo, daily_user_consumption_repo


def test_add_meal_for_user(product_dto_fix, base_user_fix, add_product_repos, db_session):
    product_rep = add_product_repos[0]
    daily_user_product_rep = add_product_repos[1]
    daily_user_consumption_rep = add_product_repos[2]
    add_meal_use_case = AddMealI(
        product_repository=product_rep,
        daily_product_repository=daily_user_product_rep,
        daily_user_consumption_repository=daily_user_consumption_rep
    )
    add_meal_use_case.execute(product_dto_fix)  # add meal for user

    commit_repos([product_rep, daily_user_product_rep, daily_user_consumption_rep])  # commit changes to db

    query_by = ("user_id", UserID(base_user_fix.id))  # query by user_id
    user_consumption: DailyUserConsumption = daily_user_consumption_rep.get_by_field_value(*query_by)

    assert user_consumption, "User consumption not found"
    assert user_consumption.summary_calories not in [0, 0.0], "Summary calories is 0"
    assert user_consumption.summary_proteins not in [0, 0.0], "Summary proteins is 0"
    assert user_consumption.summary_fats not in [0, 0.0], "Summary fats is 0"
    assert user_consumption.summary_carbohydrates not in [0, 0.0], "Summary carbohydrates is 0"
    assert user_consumption.products, "Products not found"
    assert len(user_consumption.products) == 1, "Products count is not 1"
    assert user_consumption.products[0].product_id == product_dto_fix.product_id, "Product id is not equal"
    assert user_consumption.user_id == base_user_fix.id, "User id is not equal"
