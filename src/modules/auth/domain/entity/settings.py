from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from src.core.domain.entity import Entity
from src.core.domain.value_object import PrecisedFloat
from src.modules.auth.domain.enums import GenderEnum


@dataclass
class Macro(Entity):
    settings_id: UUID

    protein: PrecisedFloat = PrecisedFloat(0.0)
    fat: PrecisedFloat = PrecisedFloat(0.0)
    carbs: PrecisedFloat = PrecisedFloat(0.0)
    calories: PrecisedFloat = PrecisedFloat(0.0)

    @staticmethod
    def _default_macro_factory(gender: GenderEnum) -> dict[str, PrecisedFloat]:
        match gender:
            case GenderEnum.FEMALE:
                return dict(
                    protein=PrecisedFloat(68.0),
                    fat=PrecisedFloat(50.0),
                    carbs=PrecisedFloat(225.0),
                    calories=PrecisedFloat(1800.0),
                )
            case GenderEnum.MALE:
                return dict(
                    protein=PrecisedFloat(90.0),
                    fat=PrecisedFloat(67.0),
                    carbs=PrecisedFloat(300.0),
                    calories=PrecisedFloat(2400.0),
                )
            case _:
                return dict(
                    protein=PrecisedFloat(70.0),
                    fat=PrecisedFloat(55.0),
                    carbs=PrecisedFloat(270.0),
                    calories=PrecisedFloat(2000.0),
                )

    @classmethod
    def create(
        cls,
        settings_id: UUID,
        gender: GenderEnum,
        protein: Optional[PrecisedFloat | float] = None,
        fat: Optional[PrecisedFloat | float] = None,
        carbs: Optional[PrecisedFloat | float] = None,
        calories: Optional[PrecisedFloat | float] = None,
    ) -> "Macro":
        if (
            protein is not None
            and fat is not None
            and carbs is not None
            and calories is not None
        ):
            return cls(
                id=cls.create_id(),
                settings_id=settings_id,
                created_at=cls.create_now_time(),
                updated_at=cls.create_now_time(),
                protein=PrecisedFloat(protein),
                fat=PrecisedFloat(fat),
                carbs=PrecisedFloat(carbs),
                calories=PrecisedFloat(calories),
            )

        return cls(
            id=cls.create_id(),
            settings_id=settings_id,
            created_at=cls.create_now_time(),
            updated_at=cls.create_now_time(),
            **cls._default_macro_factory(gender=gender),
        )


@dataclass
class UserSettings(Entity):
    user_id: UUID

    age: int  # ToDo: Set default macro values based on age
    macro: Optional[Macro] = None
    gender: GenderEnum = GenderEnum.UNSPECIFIED

    @classmethod
    def create(
        cls,
        user_id: UUID,
        age: int,
        gender: GenderEnum,
    ) -> "UserSettings":
        return cls(
            id=cls.create_id(),
            user_id=user_id,
            age=age,
            gender=gender,
            created_at=cls.create_now_time(),
            updated_at=cls.create_now_time(),
        )
