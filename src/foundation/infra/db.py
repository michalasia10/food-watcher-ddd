import uuid
from enum import Enum
from typing import Any




class LabeledEnum(Enum):
    def __str__(self):
        return self.label

    def __getattr__(self, name):
        if name == "label":
            try:
                return self._value_[1]
            except TypeError:
                return str(self.value)
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )

    @classmethod
    def _missing_(cls, value):
        raise ValueError(f"{value} is not a valid {cls.__name__.lower()}")

    @classmethod
    def _generate_next_value_(cls, name, start, count, last_values):
        value = name.lower()
        return (value, _(name))





