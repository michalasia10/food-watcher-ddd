from abc import ABCMeta
from copy import deepcopy
from uuid import UUID

from asyncpg import ObjectInUseError
from tortoise.contrib.pydantic.base import _get_fetch_fields
from tortoise.exceptions import BaseORMException
from tortoise.models import Model
from tortoise.queryset import QuerySet, QuerySetSingle
from tortoise.transactions import in_transaction

from src.core_new.domain.entity import Entity
from src.core_new.domain.errors import DBError
from src.core_new.domain.repo import IRepository


class TortoiseRepo(IRepository, metaclass=ABCMeta):
    model = Model
    entity = Entity

    @classmethod
    def _to_entity(cls, record: Model) -> Entity:
        return cls.entity(**dict(record)) if record else None

    @classmethod
    async def _prefetch(cls, queryset: QuerySet | QuerySetSingle):
        fetch_fields = _get_fetch_fields(
            cls.entity.__init__,
            cls.model
        )
        return await queryset.prefetch_related(*fetch_fields)

    @classmethod
    async def asave(cls, entity: Entity) -> Entity:
        try:
            # async with in_transaction():
                print('AAAA', entity.snapshot)
                return await cls.model.create(**entity.snapshot)



        except (BaseORMException, ObjectInUseError) as e:
            raise DBError(e)

    @classmethod
    async def aget_by_id(cls, id: UUID) -> Entity:
        model = await cls.model.get(id=id)
        return cls._to_entity(model)

    @classmethod
    async def aget_all(cls, limit=100, offset=0) -> list[Entity]:
        queryset = (
            cls.model
            .all()
            .limit(limit)
            .offset(offset)
        )
        return [
            cls._to_entity(record)
            for record in await cls._prefetch(queryset)
        ]

    @classmethod
    async def aget_first_from_filter(cls, *args, **kwargs) -> Entity:
        queryset = (
            cls.model
            .filter(*args, **kwargs)
            .first()
        )
        return cls._to_entity(await cls._prefetch(queryset))

    @classmethod
    async def aget_all_from_filter(
            cls,
            limit=100,
            offset=0,
            *args,
            **kwargs
    ) -> list[Entity]:

        queryset = (
            cls.model
            .filter(*args, **kwargs)
            .limit(limit)
            .offset(offset)
            .all()
        )
        return [
            cls._to_entity(record)
            for record in await cls._prefetch(queryset)
        ]

    @classmethod
    async def aupdate(cls, entity: Entity) -> None:
        snapshot = deepcopy(entity.snapshot)
        snapshot.pop("id")
        try:
            async with in_transaction():
                await cls.model.filter(id=entity.id).update(**snapshot)
        except BaseORMException as e:
            raise DBError(e)

    @classmethod
    async def adelete(cls, entity: Entity) -> None:
        try:
            async with in_transaction():
                await cls.model.filter(id=entity.id).delete()
        except BaseORMException as e:
            raise DBError(e)
