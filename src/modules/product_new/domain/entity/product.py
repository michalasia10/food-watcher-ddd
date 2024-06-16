from dataclasses import dataclass
from uuid import UUID

from src.core_new.domain.entity import Entity
from src.core_new.domain.value_object import PrecisedFloat


@dataclass
class Product(Entity):
    code: int | None = None
    name: str | None = None
    quantity: str | None = None
    brand: str | None = None
    size: str | None = None
    groups: str | None = None
    category: str | None = None
    user_id: UUID | None = None
    energy_kcal_100g: PrecisedFloat | None = None
    fat_100g: PrecisedFloat | None = None
    carbohydrates_100g: PrecisedFloat | None = None
    sugars_100g: PrecisedFloat | None = None
    proteins_100g: PrecisedFloat | None = None

    @classmethod
    def create(cls, *args, **kwargs) -> 'Product':
        _args = tuple(PrecisedFloat(arg) if isinstance(arg, float) else arg for arg in args)
        _kwargs = {k: PrecisedFloat(v) if isinstance(v, float) else v for k, v in kwargs.items()}

        return cls(
            id=cls.create_id(),
            updated_at=cls.create_now_time(),
            created_at=cls.create_now_time(),
            *_args,
            **_kwargs
        )
