from dataclasses import dataclass, asdict

from foundation.domain.mixins import BusinessRuleValidationMixin


@dataclass
class Entity:
    ...

    def dict(self):
        return {k: v for k, v in asdict(self).items()}


@dataclass
class AggregateRoot(BusinessRuleValidationMixin, Entity):
    """Consits of 1+ entities. Spans transaction boundaries."""
