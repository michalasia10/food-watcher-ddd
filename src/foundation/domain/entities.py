import json
import uuid
from dataclasses import dataclass, field, asdict

from .mixins import BusinessRuleValidationMixin
from .value_objects import UUID




@dataclass
class Entity:
    id: UUID = field(hash=True, default_factory=lambda: uuid.uuid4())

    def to_dict(self):
        return asdict(self)

    def to_serializer_dict(self):
        pass
        # return json.loads(json.dumps(self.to_dict(), cls=UUIDEncoder))


@dataclass
class AggregateRoot(BusinessRuleValidationMixin, Entity):
    """Consits of 1+ entities. Spans transaction boundaries."""
