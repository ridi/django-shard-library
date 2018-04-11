
from shard.managers import BaseShardManager
from shard_static_sync.exceptions import NotExistsOriginalDataException


def _wrap_for_static(func_name):
    def wrapped(self, *args, **kwargs):
        if not self.model.diffusible:
            raise NotExistsOriginalDataException()

        return getattr(self.get_queryset(), func_name)(*args, **kwargs)

    wrapped.__name__ = func_name
    return wrapped


class ShardStaticManager(BaseShardManager):
    filter = _wrap_for_static('filter')
    get = _wrap_for_static('get')
    create = _wrap_for_static('create')
    get_or_create = _wrap_for_static('get_or_create')
    update_or_create = _wrap_for_static('update_or_create')
