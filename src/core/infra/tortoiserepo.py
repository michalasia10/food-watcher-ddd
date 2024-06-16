from abc import ABCMeta
from copy import deepcopy
from typing import TypeVar, Generic, Type, List, Optional, Any
from uuid import UUID

from asyncpg import ObjectInUseError
from loguru import logger
from tortoise.contrib.pydantic.base import _get_fetch_fields
from tortoise.exceptions import BaseORMException
from tortoise.fields import Field, ReverseRelation
from tortoise.models import Model
from tortoise.queryset import QuerySet, QuerySetSingle
from tortoise.transactions import in_transaction

from src.core.domain.entity import Entity
from src.core.domain.errors import DBError
from src.core.domain.repo import IRepository
from src.core.domain.value_object import PrecisedFloat

ModelType = TypeVar('ModelType', bound=Model)
EntityType = TypeVar('EntityType', bound=Entity)


def _get_fetch_fields(
        pydantic_class: "Type[PydanticModel]", model_class: "Type[Model]"
) -> List[str]:
    """
    Recursively collect fields needed to fetch
    :param pydantic_class: The pydantic model class
    :param model_class: The tortoise model class
    :return: The list of fields to be fetched
    """
    fetch_fields = []
    for field_name, field_type in pydantic_class.__annotations__.items():
        if field_name in model_class._meta.fetch_fields:
            fetch_fields.append(field_name)
    return fetch_fields


class TortoiseRepo(Generic[ModelType, EntityType], IRepository, metaclass=ABCMeta):
    model = ModelType
    entity = EntityType

    @staticmethod
    def _convert_key(key: str) -> str:
        return key[1:] if key.startswith('_') else key

    @classmethod
    def _to_entity(cls, record: ModelType) -> EntityType | None:

        def convert_value(value) -> PrecisedFloat | list[dict] | None:
            if isinstance(value, float):
                return PrecisedFloat(value)
            return value

        def should_be_skipped(key: str) -> bool:
            return key in ['_partial', '_saved_in_db', '_custom_generated_pk']

        if record:
            _dict = {
                cls._convert_key(key): convert_value(value)
                for key, value in vars(record).items() if not should_be_skipped(key)
            }
            return cls.entity(**_dict)

        return None

    @classmethod
    async def _prefetch(cls, queryset: QuerySet | QuerySetSingle, fetch_fields: Optional[list[str]] = None):
        fetch_fields = fetch_fields or _get_fetch_fields(
            cls.entity.__init__,
            cls.model
        )
        return await queryset.prefetch_related(*fetch_fields)

    @classmethod
    async def _fetch_related(cls, queryset: QuerySet | QuerySetSingle, fetch_fields: Optional[list[str]] = None):
        fetch_fields = fetch_fields or _get_fetch_fields(
            cls.entity.__init__,
            cls.model
        )
        for field in fetch_fields:
            await queryset.fetch_related(field)

    @classmethod
    def convert_snapshot(cls, snapshot: dict) -> dict:
        snapshot = deepcopy(snapshot)

        def _convert_value(value: Any):
            if isinstance(value, ReverseRelation):
                return [{cls._convert_key(k): _convert_value(v) for k, v in vars(val).items()} for val in value]
            if isinstance(value, Model):
                return {cls._convert_key(k): v for k, v in vars(value).items()}

            return value

        return {cls._convert_key(key): _convert_value(value) for key, value in snapshot.items()}

    @classmethod
    async def asave(cls, entity: EntityType) -> EntityType:
        try:
            async with in_transaction():
                entity = await cls.model.create(**entity.snapshot)
                logger.info("Object {entity} saved in db", entity=entity)
                return entity

        except (BaseORMException, ObjectInUseError) as e:
            raise DBError(e)

    @classmethod
    async def aget_by_id(cls, id: UUID, fetch_fields: Optional[list[str]] = None) -> EntityType | None:
        model = await cls.model.get(id=id)

        await cls._fetch_related(model, fetch_fields)

        return cls._to_entity(model)

    @classmethod
    async def aget_all(cls, limit=100, offset=0, fetch_fields: Optional[list[str]] = None) -> list[EntityType]:
        queryset = (
            cls.model
            .all()
            .limit(limit)
            .offset(offset)
        )
        return [
            cls._to_entity(record)
            for record in await cls._prefetch(queryset, fetch_fields)
        ]

    @classmethod
    async def aget_first_from_filter(
            cls,
            fetch_fields: Optional[list[str]] = None,
            *args,
            **kwargs
    ) -> EntityType | None:

        queryset = (
            cls.model
            .filter(*args, **kwargs)
            .first()
        )
        return cls._to_entity(await cls._prefetch(queryset, fetch_fields))

    @classmethod
    async def aget_all_from_filter(
            cls,
            limit=100,
            offset=0,
            fetch_fields: Optional[list[str]] = None,
            *args,
            **kwargs
    ) -> list[EntityType]:

        queryset = (
            cls.model
            .filter(*args, **kwargs)
            .limit(limit)
            .offset(offset)
            .all()
        )
        return [
            cls._to_entity(record)
            for record in await cls._prefetch(queryset, fetch_fields)
        ]

    @classmethod
    async def aupdate(cls, entity: EntityType) -> None:
        snapshot = deepcopy(entity.snapshot)
        clean_snapshot = {
            k: v for k, v in snapshot.items()
            if k != 'id' and not isinstance(v, Field) and not isinstance(v, ReverseRelation)
        }
        try:
            async with in_transaction():
                await cls.model.filter(id=entity.id).update(**clean_snapshot)
        except BaseORMException as e:
            raise DBError(e)

    @classmethod
    async def adelete(cls, entity: EntityType) -> None:
        try:
            async with in_transaction():
                await cls.model.filter(id=entity.id).delete()
        except BaseORMException as e:
            raise DBError(e)
