from contextvars import ContextVar
from typing import TypeVar, Any, NoReturn, Callable, Generic, Tuple
from uuid import UUID as UUDIBase

from sqlalchemy.orm import Session, joinedload, class_mapper

from src.foundation.domain.entity import Entity as E
from src.foundation.infra.db import Base

Entity = TypeVar("Entity", bound=E)
UUID = TypeVar("UUID", bound=UUDIBase)
Model = Callable[..., Base]


def to_dict_recursive(obj, seen=None):
    if seen is None:
        seen = {}

    if obj in seen:
        return seen[obj]

    seen[obj] = {}

    mapper = class_mapper(obj.__class__)

    for column in mapper.columns:
        seen[obj][column.key] = getattr(obj, column.key)

    for relationship in mapper.relationships:
        related_obj = getattr(obj, relationship.key)
        if related_obj is not None:
            if isinstance(related_obj, list):
                seen[obj][relationship.key] = [to_dict_recursive(child, seen) for child in related_obj]
            else:
                seen[obj][relationship.key] = to_dict_recursive(related_obj, seen)

    return seen[obj]


def clean_dict(dictionary):
    if isinstance(dictionary, dict):
        return {key: clean_dict(value) for key, value in dictionary.items() if value is not None}
    elif isinstance(dictionary, list):
        return [clean_dict(item) for item in dictionary if item is not None]
    else:
        return dictionary


class Repository(Generic[Entity, UUID]):
    model = Model
    entity = Entity

    def __init__(self, db_session: ContextVar):
        self._session = db_session

    @property
    def session(self) -> Session:
        return self._session.get()

    @staticmethod
    def data_to_entity(data: Base, entity: [Entity]) -> Entity:
        data_as_dict = to_dict_recursive(data)
        return entity(**data_as_dict)

    def entity_to_model(self, entity: [Entity], model: Model | None = None, update=False) -> [Base]:
        entity_dict = {key: value for key, value in vars(entity).copy().items() if not key.startswith("_")}
        for key, value in entity_dict.items():
            if hasattr(getattr(entity, key), "Meta") and hasattr(getattr(entity, key).Meta, "orm_model"):
                child = self.entity_to_model(getattr(entity, key), getattr(entity, key).Meta.orm_model, update=update)
                child.id = None
                entity_dict[key] = child
            if isinstance(value, list):
                children = [self.entity_to_model(item, update=update) for item in getattr(entity, key)]
                [setattr(child, "id", None) for child in children]
                entity_dict[key] = children

        if update:
            entity_dict["id"] = None

        entity_dict = clean_dict(entity_dict)
        if hasattr(entity, "Meta") and hasattr(entity.Meta, "orm_model"):
            return entity.Meta.orm_model(**entity_dict)

        elif model:
            return model(**entity_dict)

        return self.model(**entity_dict)

    def get_by_id(self, id: UUID, raw=False) -> NotImplementedError | Entity | None:
        if hasattr(self.model, "Meta") and hasattr(self.model.Meta, "children"):
            relation = [getattr(self.model, child) for child in self.model.Meta.children]
        else:
            relation = []

        if relation:
            data = self.session.query(self.model).options(joinedload(*relation)).filter_by(id=str(id)).first()
        else:
            data = self.session.query(self.model).filter_by(id=str(id)).first()

        if raw:
            return data

        return self.data_to_entity(data, self.entity) if data else None

    def create(self, entity: Entity, raw=False) -> Entity:
        model = self.entity_to_model(entity)
        self.session.add(model)
        self.commit()
        return self.get_by_id(model.id, raw)

    def update(self, entity: Entity, raw=False) -> tuple[Any] | Entity:
        record = self.session.query(self.model).filter_by(id=str(entity.id)).first()
        if record is None:
            raise Exception(f"Record with id {entity.id} not found")

        for key, value in vars(entity).items():
            if isinstance(value, list):
                values_as_model = [self.entity_to_model(item, update=True) for item in value if
                                   hasattr(item, "Meta") and hasattr(item.Meta, "orm_model")]
                for value_as_model in values_as_model:
                    getattr(record, key).append(value_as_model)
            elif hasattr(value, "Meta") and hasattr(value.Meta, "orm_model"):
                value_as_model = self.entity_to_model(value, update=True)
                setattr(record, key, value_as_model)
            elif value is None or not value:
                continue
            else:
                setattr(record, key, value)
            print(f"Record with id {entity.id} updated for key {key} with value {value}")
        if raw:
            return record
        return entity

    def get_by_field_value(self, field: str, value: Any, raw=False) -> tuple[Any] | None | Any:
        if hasattr(self.model, "Meta") and hasattr(self.model.Meta, "children"):
            relation = [getattr(self.model, child) for child in self.model.Meta.children]
        else:
            relation = []

        if relation:
            data = self.session.query(self.model).options(joinedload(*relation)).filter_by(**{field: value}).first()
        else:
            data = self.session.query(self.model).filter_by(**{field: value}).first()

        if raw:
            return data if data else None

        return self.data_to_entity(data, self.entity) if data else None

    def get_by_field_values(self, raw=False, **kwargs) -> tuple[Any] | None | Any:
        if hasattr(self.model, "Meta") and hasattr(self.model.Meta, "children"):
            relation = [getattr(self.model, child) for child in self.model.Meta.children]
        else:
            relation = []

        if relation:
            data = self.session.query(self.model).options(joinedload(*relation)).filter_by(**kwargs).first()
        else:
            data = self.session.query(self.model).filter_by(**kwargs).first()

        if raw:
            return data if data else None

        return self.data_to_entity(data, self.entity) if data else None

    def delete(self, id: Entity) -> NoReturn:
        raise NotImplementedError

    def exists(self, field: str, value: Any) -> bool:
        return bool(self.session.query(self.model).filter_by(**{field: value}).first())

    def get_all(self) -> list[Entity]:
        data = self.session.query(self.model).all()
        return [self.data_to_entity(dat, self.entity) for dat in data]

    def get_all_pagination(self, skip: int, limit: int, **kwargs) -> list[Entity]:
        if hasattr(self.model, "Meta") and hasattr(self.model.Meta, "children"):
            relation = [getattr(self.model, child) for child in self.model.Meta.children]
        else:
            relation = []

        query = self.session.query(self.model)

        if relation:
            query = query.options(joinedload(*relation))

        if kwargs:
            query = query.filter_by(**kwargs)

        if limit:
            query = query.limit(limit)

        if skip:
            query = query.offset(skip)

        data = query.all()
        return [self.data_to_entity(dat, self.entity) for dat in data]

    def commit(self):
        self.session.commit()
