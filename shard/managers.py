import typing

from django.db.models.manager import Manager

from shard.exceptions import NotExistsOriginalDataException
from shard.queryset import ShardQuerySet
from shard.utils.shard import get_shard_by_shard_key_and_shard_group
from shard.utils.shard_key import get_shard_key_from_kwargs, mod_shard_key_by_replica_count

__all__ = ('ShardStaticManager', 'ShardManager', )


def _wrap(func_name):
    def wrapped(self, *args, **kwargs):
        shard_key = get_shard_key_from_kwargs(model=self.model, **kwargs)
        return getattr(self.get_queryset(shard_key=shard_key), func_name)(*args, **kwargs)

    wrapped.__name__ = func_name
    return wrapped


def _static_wrap(func_name):
    def wrapped(self, *args, **kwargs):
        if not self.model.diffusible:
            raise NotExistsOriginalDataException()

        return getattr(self.get_queryset(), func_name)(*args, **kwargs)

    wrapped.__name__ = func_name
    return wrapped


class BaseShardManager(Manager):
    def shard(self, shard_key):
        _shard_key = mod_shard_key_by_replica_count(shard_key, self.model.shard_group)
        shard = get_shard_by_shard_key_and_shard_group(shard_key=_shard_key, shard_group=self.model.shard_group)
        return self.get_queryset().using(shard)

    def get_queryset(self, shard_key=None):
        hints = {'shard_key': shard_key}
        return ShardQuerySet(model=self.model, hints=hints)


class ShardStaticManager(BaseShardManager):
    filter = _static_wrap('filter')
    get = _static_wrap('get')
    create = _static_wrap('create')
    get_or_create = _static_wrap('get_or_create')
    update_or_create = _static_wrap('update_or_create')


class ShardManager(BaseShardManager):
    def raw(self, shard_key: int, query: str):
        return self.shard(shard_key=shard_key).raw(query)

    def bulk_create(self, shard_key: int, objs: typing.List, batch_size: int):
        return self.shard(shard_key=shard_key).bulk_create(objs=objs, batch_size=batch_size)

    filter = _wrap('filter')
    get = _wrap('get')
    create = _wrap('create')
    get_or_create = _wrap('get_or_create')
    update_or_create = _wrap('update_or_create')
