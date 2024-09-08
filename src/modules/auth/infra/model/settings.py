from tortoise import fields
from uuid6 import uuid6

from src.core.infra.model import BaseModel
from src.modules.auth.domain.enums import GenderEnum


class Macro(BaseModel):
    proteins = fields.FloatField(null=False)
    fats = fields.FloatField(null=False)
    carbs = fields.FloatField(null=False)
    calories = fields.FloatField(null=False)

    settings = fields.OneToOneField(
        "auth.UserSettings",
        related_name="macro",
        to_field="id",
        default=uuid6,
        db_constraint=True,
    )

    class Meta:
        app = "auth"
        table = "macro"


class UserSettings(BaseModel):
    age = fields.IntField(null=False)
    gender = fields.CharEnumField(
        enum_type=GenderEnum,
        default=GenderEnum.UNSPECIFIED.value,
    )

    user = fields.OneToOneField(
        "auth.User",
        related_name="settings",
        to_field="id",
        default=uuid6,
        db_constraint=True,
    )

    class Meta:
        app = "auth"
        table = "settings"
