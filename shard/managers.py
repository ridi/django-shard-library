from django.db.models.manager import Manager

from shard.queryset import ShardQuerySet
from shard.utils.shard_key import get_shard_key_from_kwargs

__all__ = ('ShardManager', )


def _wrap(func_name):
    def wrapped(self, *args, **kwargs):
        shard_key = get_shard_key_from_kwargs(model=self.model, **kwargs)
        return getattr(self.get_queryset(shard_key=shard_key), func_name)(*args, **kwargs)

    wrapped.__name__ = func_name
    return wrapped


class ShardManager(Manager):
    def shard(self, shard_key):
        return self.get_queryset(shard_key=shard_key)

    def get_queryset(self, shard_key=None):
        hints = {'shard_key': shard_key}
        return ShardQuerySet(model=self.model, hints=hints)

    filter = _wrap('filter')
    get = _wrap('get')
    create = _wrap('create')
    get_or_create = _wrap('get_or_create')
    update_or_create = _wrap('update_or_create')
