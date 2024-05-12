from fastapi import HTTPException
from pydantic import BaseModel

from .filters import UserFilter


class QueryValidator:
    """
    A validator for a query string that starts with `?filter`. Validates that the query string contains only
    valid fields and that the field types are correct. Nested fields can be accessed using dot notation (e.g. nested_field.subfield).

    param filter_model: The Pydantic model to validate the filter against.
    type filter_model: Type[BaseModel | dataclass]

    Example:
     ?filter=name=John&age=25
     ?filter=name=John&city=New%20York
     ?filter=name=John&city=New%20York&state=NY
     ?filter=name=John&city=New%20York&state=NY&zip_code=10001
     ?filter=created_at=2022-02-15T12:00:00Z
     ?filter=created_at=2022-02-15T12:00:00Z&status=active
     ?filter=created_at=2022-02-15T12:00:00Z&status=active&category=electronics
     ?filter=created_at=2022-02-15T12:00:00Z&status=active&category=electronics&price=1000.00
     ?filter=created_at=2022-02-15T12:00:00Z&status=active&category=electronics&price=1000.00&manufacturer=Apple
     ?filter=created_at=2022-02-15T12:00:00Z&status=active&category=electronics&price=1000.00&manufacturer=Apple&color=red



    """

    def __init__(self, filter_model):
        self.filter_model = filter_model

    def validate(self, filter_query: str | None) -> dict:
        if not filter_query:
            return {}

        filters = self._parse_filter_query(filter_query)
        filtered_fields = self._filter_allowed_fields(filters.keys())
        return {field: filters[field] for field in filtered_fields}

    def _parse_filter_query(self, filter_query: str) -> dict:
        parsed_query = {}
        for param in filter_query.split("&"):
            filter_key, filter_value = param.split("=", 1)
            parsed_query[filter_key] = self._parse_field_value(filter_key, filter_value)
        return parsed_query

    def _parse_field_value(self, filter_key: str, filter_value: str) -> str | dict:
        if "." in filter_key:
            nested_fields = filter_key.split(".")
            field_name = nested_fields.pop(0)
            return {
                field_name: self._parse_field_value(
                    ".".join(nested_fields), filter_value
                )
            }

        field = self._get_field_by_alias(filter_key)
        self._validate_field_type(field, filter_value, filter_key)
        return filter_value

    def _get_field_by_alias(self, filter_key: str):
        field = next(
            (f for f in self.filter_model.__fields__.values() if f.alias == filter_key),
            None,
        )
        if not field:
            raise HTTPException(
                status_code=400, detail=f"Invalid field '{filter_key}' in filter"
            )
        return field

    def _validate_field_type(self, field, filter_value, filter_key):
        if isinstance(field.type_, type) and issubclass(field.type_, BaseModel):
            try:
                field.type_(**filter_value)
            except:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid value '{filter_value}' for field '{filter_key}' in filter",
                )

    def _filter_allowed_fields(self, fields):
        return set(fields) & set(self.filter_model.__fields__.keys())


user_query_validator = QueryValidator(UserFilter)
