from dataclasses import dataclass

from src.core_new.domain.entity import Entity


@dataclass
class Product(Entity):
    code: int | None = None
    name: str | None = None
    quantity: str | None = None
    brand: str | None = None
    size: str | None = None
    groups: str | None = None
    category: str | None = None
    energy_kcal_100g: float | None = None
    fat_100g: float | None = None
    carbohydrates_100g: float | None = None
    sugars_100g: float | None = None
    proteins_100g: float | None = None

    @classmethod
    def create(cls, *args, **kwargs) -> 'Product':
        return cls(
            id=cls.create_id(),
            updated_at=cls.create_now_time(),
            created_at=cls.create_now_time(),
            *args,
            **kwargs
        )
