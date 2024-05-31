from src.core_new.domain.errors import DBErrorNotFound, BadPermissions


class ProductNotFound(DBErrorNotFound): ...


class ProductNotRecordOwner(BadPermissions): ...


class DailyUserConsumptionNotRecordOwner(BadPermissions): ...
