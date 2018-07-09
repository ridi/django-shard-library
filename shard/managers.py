import typing
from django.db.models.manager import Manager

from shard.queryset import ShardQuerySet
from shard.strategy.routing.random import RandomReadStrategy
from shard.utils.shard import get_shard_by_shard_key_and_shard_group
from shard.utils.shard_key import get_shard_key_from_kwargs

__all__ = ('ShardManager',)


def _wrap(func_name):
    def wrapped(self, *args, **kwargs):
        shard_key = get_shard_key_from_kwargs(model=self.model, **kwargs)
        is_fresh = kwargs.get('is_fresh', False)
        return getattr(self.get_queryset(shard_key=shard_key, is_fresh=is_fresh), func_name)(*args, **kwargs)

    wrapped.__name__ = func_name
    return wrapped


class BaseShardManager(Manager):
    _strategy = RandomReadStrategy

    def shard(self, shard: str, is_fresh: bool = False):
        if not is_fresh:
            shard = self._strategy.pick_read_db(shard)

        return self.get_queryset().using(shard)

    def get_queryset(self, shard_key=None, is_fresh: bool = False):
        hints = {'shard_key': shard_key, 'is_fresh': is_fresh, }
        return ShardQuerySet(model=self.model, hints=hints)


class ShardManager(BaseShardManager):
    def raw(self, shard_key: int, query: str):
        return self.shard(shard=get_shard_by_shard_key_and_shard_group(shard_key=shard_key, shard_group=self.model.shard_group)).raw(query)

    def bulk_create(self, shard_key: int, objs: typing.List, batch_size: int):
        return self.shard(shard=get_shard_by_shard_key_and_shard_group(shard_key=shard_key, shard_group=self.model.shard_group)) \
            .bulk_create(objs=objs, batch_size=batch_size)

    filter = _wrap('filter')
    get = _wrap('get')
    create = _wrap('create')
    get_or_create = _wrap('get_or_create')
    update_or_create = _wrap('update_or_create')
