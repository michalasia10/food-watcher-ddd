import json
import uuid
from dataclasses import dataclass, field, asdict

from .mixins import BusinessRuleValidationMixin
from .value_objects import UUID


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return obj.hex
        return json.JSONEncoder.default(self, obj)


@dataclass
class Entity:
    id: UUID = field(hash=True, default_factory=lambda: uuid.uuid4())

    def to_dict(self):
        return asdict(self)

    def to_serializer_dict(self):
        return json.loads(json.dumps(self.to_dict(), cls=UUIDEncoder))


@dataclass
class AggregateRoot(BusinessRuleValidationMixin, Entity):
    """Consits of 1+ entities. Spans transaction boundaries."""
