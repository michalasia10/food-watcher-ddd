from src.modules.product.domain.entity.product import Product


def test_create_product_entity():
    product = Product.create(
        code=1,
        name="test",
        quantity="1",
        brand="test",
        size="1",
        groups="test",
        category="test",
        energy_kcal_100g=1.0,
        fat_100g=1.0,
        carbohydrates_100g=1.0,
        sugars_100g=1.0,
        proteins_100g=1.0
    )
    assert product.code == 1
    assert product.name == "test"
    assert product.quantity == "1"
    assert product.brand == "test"
    assert product.size == "1"
    assert product.groups == "test"
    assert product.category == "test"
    assert product.energy_kcal_100g == 1.0
    assert product.fat_100g == 1.0
    assert product.carbohydrates_100g == 1.0
    assert product.sugars_100g == 1.0
    assert product.proteins_100g == 1.0
    assert product.id is not None
    assert product.updated_at is not None
    assert product.created_at is not None



