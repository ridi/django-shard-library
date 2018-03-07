from typing import List, Dict

from django.conf import settings

from shard.utils.memorize import memorize
from shard.constants import DATABASE_CONFIG_MASTER, DATABASE_CONFIG_SHARD_GROUP, DATABASE_CONFIG_SHARD_NUMBER

__all__ = ('get_master_databases', 'get_master_databases_by_shard_group', 'get_slave_databases_by_master', )


@memorize
def get_master_databases(without_shard: bool = True) -> List:
    databases = _get_databases()

    result = []
    for key, config in databases.items():
        if config.get(DATABASE_CONFIG_MASTER):
            continue

        if without_shard:
            if config.get(DATABASE_CONFIG_SHARD_GROUP) or config.get(DATABASE_CONFIG_SHARD_NUMBER):
                continue

        result.append(key)

    return result


@memorize
def get_master_databases_by_shard_group(shard_group: str) -> List:
    databases = _get_databases()
    shards = []

    for key, config in databases.items():
        if config.get(DATABASE_CONFIG_MASTER):
            continue

        _group = config.get(DATABASE_CONFIG_SHARD_GROUP, None)
        if _group is None or _group != shard_group:
            continue

        shards.append(key)

    shards = sorted(shards, key=lambda shard: databases[shard][DATABASE_CONFIG_SHARD_NUMBER])
    return shards


@memorize
def get_slave_databases_by_master(master: str) -> List:
    result = []
    for key, config in _get_databases().items():
        _master = config.get(DATABASE_CONFIG_MASTER, None)
        if _master is None or _master != master:
            continue

        result.append(key)

    return result


def _get_databases() -> Dict:
    return settings.DATABASES
