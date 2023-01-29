from dataclasses import dataclass, asdict


@dataclass
class Entity:
    ...

    def dict(self):
        return {k: v for k, v in asdict(self).items()}
