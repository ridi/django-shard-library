from django.conf import settings

from shard.exceptions import NotShardingModelException, RequireShardKeyException
from shard.mixins import ShardMixin

__all__ = ('get_shard_key_from_kwargs', 'get_shard_key_from_instance', 'mod_shard_key_by_replica_count', )

SHARD_REPLICA_COUNT_SETTING = 'SHARD_REPLICA_COUNT_SETTING'
DEFAULT_REPLICA_COUNT = 1024


def get_shard_key_from_kwargs(model, **kwargs) -> int:
    _validate_shard_model(model)

    if model.shard_key_name not in kwargs:
        raise RequireShardKeyException()

    return kwargs[model.shard_key_name]


def get_shard_key_from_instance(instance: ShardMixin) -> int:
    return instance.get_shard_key()


def mod_shard_key_by_replica_count(shard_key: int, shard_group: str) -> int:
    return _calc_shard_key(shard_key, shard_group)


def _validate_shard_model(model):
    if not issubclass(model, ShardMixin):
        raise NotShardingModelException()

    if model.shard_group is None or model.shard_key_name is None:
        raise NotShardingModelException()


def _calc_shard_key(key: int, shard_group: str) -> int:
    return int(key % _get_replica_count(shard_group=shard_group))


def _get_replica_count(shard_group: str) -> int:
    replica_settings = _get_shard_replica_settings()
    return replica_settings.get(shard_group, DEFAULT_REPLICA_COUNT)


def _get_shard_replica_settings():
    return getattr(settings, SHARD_REPLICA_COUNT_SETTING, {})
