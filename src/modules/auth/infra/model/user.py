from tortoise import fields

from src.core.infra.model import BaseModel
from src.modules.auth.domain.enums import StatusEnum, TypeEnum


class User(BaseModel):
    username = fields.CharField(null=False, max_length=255)
    password = fields.CharField(null=False, max_length=255)
    email = fields.CharField(null=False, max_length=255)  # ToDo: Add email validation
    first_name = fields.CharField(null=True, max_length=255)
    last_name = fields.CharField(null=True, max_length=255)
    status = fields.CharEnumField(
        enum_type=StatusEnum, default=StatusEnum.INACTIVE.value
    )
    type = fields.CharEnumField(enum_type=TypeEnum, default=TypeEnum.USER.value)

    # daily_user_consumptions = relationship(
    #     "DailyUserConsumption", back_populates="user"
    # )
    # settings = relationship("UserSettings", back_populates="user")
    # messages = relationship("Message", back_populates="user")

    class Meta:
        app = "auth"
        table = "user"
