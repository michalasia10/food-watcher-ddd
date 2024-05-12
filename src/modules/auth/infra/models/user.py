# from tortoise import fields
#
# from core_new.infra.model import BaseModel
# from modules.auth_new.domain.enums import StatusEnum, TypeEnum


class User:
    pass
    # username = fields.CharField(null=False, max_length=255)
    # password = fields.CharField(null=False, max_length=255)
    # email = fields.CharField(null=False, max_length=255)  # ToDo: Add email validation
    # first_name = fields.CharField(null=True, max_length=255)
    # last_name = fields.CharField(null=True, max_length=255)
    # status = fields.CharEnumField(enum_type=StatusEnum, default=StatusEnum.INACTIVE)
    # type = fields.CharEnumField(enum_type=TypeEnum, default=TypeEnum.USER)
    #
    # # daily_user_consumptions = relationship(
    # #     "DailyUserConsumption", back_populates="user"
    # # )
    # # settings = relationship("UserSettings", back_populates="user")
    # # messages = relationship("Message", back_populates="user")
    #
    # class Meta:
    #     app = 'auth'

# class UserSettings(Base):
#     __tablename__ = "user_settings"
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
#
#     user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), primary_key=True)
#     user = relationship("User", back_populates="settings")
#     daily_calories = Column(Float(), nullable=True)
#     daily_proteins = Column(Float(), nullable=True)
#     daily_fats = Column(Float(), nullable=True)
#     daily_carbohydrates = Column(Float(), nullable=True)
