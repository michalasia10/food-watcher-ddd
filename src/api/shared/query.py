import datetime
import typing

from pydantic import BaseModel, root_validator, ValidationError, constr


class QueryFilter(BaseModel):
    field: str
    operator: constr(
        regex=r"^(includes|contains|<|<=|>=|>)$"
    )
    value: typing.Union[str, int, datetime.date]

    @root_validator
    def validate_value(cls, values):
        operator = values.get("operator")
        value = values.get("value")

        if not isinstance(value, (int, datetime.date)):
            if operator in {"<=", "<", ">", ">="}:
                raise ValidationError("For operator {} value must be a number".format(operator))
        return values
