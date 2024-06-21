from tortoise import fields
from tortoise.models import Model
from uuid6 import uuid6


class BaseModel(Model):
    id = fields.UUIDField(
        pk=True,
        default=uuid6,
        null=False,
        generated=False,
        unique=True,
    )
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return f'.::{self.__class__.__name__}::..::{self.id}::.'

    class Meta:
        abstract = True
