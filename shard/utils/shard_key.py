from shard.exceptions import NotShardingModelException, RequireShardKeyException
from shard.mixins import ShardMixin

__all__ = ('get_shard_key_from_kwargs', 'get_shard_key_from_instance', )


def get_shard_key_from_kwargs(model, **kwargs) -> int:
    _validate_shard_model(model)

    if model.shard_key_name not in kwargs:
        raise RequireShardKeyException()

    return kwargs[model.shard_key_name]


def get_shard_key_from_instance(instance: ShardMixin) -> int:
    return instance.get_shard_key()


def _validate_shard_model(model):
    if not issubclass(model, ShardMixin):
        raise NotShardingModelException()

    if model.shard_group is None or model.shard_key_name is None:
        raise NotShardingModelException()
