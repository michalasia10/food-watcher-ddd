from enum import Enum


class StatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class TypeEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"
    DIETITIAN = "dietitian"
