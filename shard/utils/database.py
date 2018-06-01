from typing import Dict, List

from django.conf import settings

from shard.constants import DATABASE_CONFIG_MASTER, DATABASE_CONFIG_SHARD_GROUP, DATABASE_CONFIG_SHARD_NUMBER
from shard.utils.memorize import memorize

__all__ = (
    'get_shard_groups', 'get_master_databases', 'get_master_databases_for_shard', 'get_master_databases_by_shard_group',
    'get_slave_databases_by_master', 'get_tables',
)


@memorize
def get_shard_groups() -> List[str]:
    databases = _get_databases()
    groups = []

    for config in databases.values():
        if config.get(DATABASE_CONFIG_MASTER):
            continue

        if config.get(DATABASE_CONFIG_SHARD_GROUP) is None or config.get(DATABASE_CONFIG_SHARD_NUMBER) is None:
            continue

        database = config.get(DATABASE_CONFIG_SHARD_GROUP)
        if database in groups:
            continue

        groups.append(database)

    return groups


@memorize
def get_master_databases(without_shard: bool = True) -> List[str]:
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
def get_master_databases_for_shard() -> List[str]:
    databases = _get_databases()
    shards = []

    for key, config in databases.items():
        if config.get(DATABASE_CONFIG_MASTER):
            continue

        if config.get(DATABASE_CONFIG_SHARD_GROUP) is None or config.get(DATABASE_CONFIG_SHARD_NUMBER) is None:
            continue

        shards.append(key)

    shards = sorted(
        shards, key=lambda shard: (databases[shard][DATABASE_CONFIG_SHARD_GROUP], databases[shard][DATABASE_CONFIG_SHARD_NUMBER])
    )
    return shards


@memorize
def get_master_databases_by_shard_group(shard_group: str) -> List[str]:
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
def get_slave_databases_by_master(master: str) -> List[str]:
    result = []
    for key, config in _get_databases().items():
        _master = config.get(DATABASE_CONFIG_MASTER, None)
        if _master is None or _master != master:
            continue

        result.append(key)

    return result


@memorize
def get_tables(databases: List) -> List[str]:
    result = []

    _databases = _get_databases()
    for database in databases:
        result.append(_databases[database]['NAME'])

    return result


def _get_databases() -> Dict:
    return settings.DATABASES
