
from shard.mixins import ShardMixin
from shard.utils.shard_key import get_shard_key_from_instance, mod_shard_key_by_replica_count
from shard.utils.database import get_master_databases_by_shard_group

__all__ = (
    'get_shard_by_shard_key_and_shard_group', 'get_shard_by_instance',
)


def get_shard_by_shard_key_and_shard_group(shard_key: int, shard_group: str) -> str:
    key = mod_shard_key_by_replica_count(shard_key=shard_key, shard_group=shard_group)
    databases = get_master_databases_by_shard_group(shard_group=shard_group)
    return databases[_calc_shard(shard_key=key, shard_count=len(databases))]


def get_shard_by_instance(instance: ShardMixin) -> str:
    key = mod_shard_key_by_replica_count(shard_key=get_shard_key_from_instance(instance=instance), shard_group=instance.shard_group)
    databases = get_master_databases_by_shard_group(shard_group=instance.shard_group)
    return databases[_calc_shard(shard_key=key, shard_count=len(databases))]


def _calc_shard(shard_key: int, shard_count: int) -> int:
    return int(shard_key % shard_count)
