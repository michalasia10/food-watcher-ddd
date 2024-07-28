import json
from datetime import datetime, date
from typing import Any
from uuid import UUID

from uuid6 import UUID as UUIDv6


class CustomJsonEncoder(json.JSONEncoder):
    """
    Custom JSON encoder that serializes datetime and date objects to ISO format.
    """

    def default(self, obj: Any) -> Any:
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, (UUID, UUIDv6)):
            return obj.hex

        return super().default(obj)
