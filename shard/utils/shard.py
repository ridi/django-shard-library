from shard.mixins import ShardMixin
from shard.providers import pool_provider
from shard.utils.shard_key import get_shard_key_from_instance
from shard.utils.database import get_master_databases_by_shard_group

__all__ = ('get_shard_by_shard_key_and_shard_group', 'get_shard_by_instance', )


def get_shard_by_shard_key_and_shard_group(shard_key: int, shard_group: str) -> str:
    databases = get_master_databases_by_shard_group(shard_group=shard_group)
    shard_index = pool_provider.get_shard_index(shard_group=shard_group, shard_key=shard_key)
    return databases[shard_index]


def get_shard_by_instance(instance: ShardMixin) -> str:
    databases = get_master_databases_by_shard_group(shard_group=instance.shard_group)
    shard_index = pool_provider.get_shard_index(shard_key=get_shard_key_from_instance(instance=instance), shard_group=instance.shard_group)
    return databases[shard_index]
