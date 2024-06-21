from src.core.domain.errors import DBErrorNotFound, BadPermissions, ValidationError


class ProductForRecipeNotFound(DBErrorNotFound): ...


class RecipeNotFound(DBErrorNotFound): ...


class RecipeNotRecordOwner(BadPermissions): ...


class ProductForRecipeNotRecordOwner(BadPermissions): ...


class ProductNotFound(ValidationError): ...
