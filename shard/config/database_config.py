from typing import Optional, Tuple, Dict, List

from dj_database_url import config

from shard.constants import DATABASE_CONFIG_MASTER, DATABASE_CONFIG_SHARD_GROUP, DATABASE_CONFIG_SHARD_NUMBER
from shard.exceptions import RequireMasterConfigException

__all__ = ('make_shard_configuration', 'make_replication_configuration', )


def make_shard_configuration(shard_group: str, shard_options: Dict, shards: List) -> Dict:
    configuration = {}
    database_name = shard_options['database_name']
    logical_count_per_shard = _get_logical_count_per_shard(logical_count=shard_options['logical_count'], shard_count=len(shards))

    for index, shard_config in enumerate(shards):
        start, end = _get_logical_range(index, logical_count_per_shard)
        for logical_index in range(start, end):
            shard_name = _make_shard_name(shard_group=shard_group, shard_index=index, logical_index=logical_index)
            replication_config = {
                'master': _make_shard_database_url(origin=shard_config['master'], database_name=database_name, logical_index=logical_index),
                'slaves': [
                    _make_shard_database_url(origin=slave_database_url, database_name=database_name, logical_index=logical_index)
                    for slave_database_url in shard_config.get('slaves', [])
                ],
            }

            configuration.update(make_replication_configuration(key=shard_name, replication_config=replication_config, options={
                'shard_group': shard_group, 'shard_number': logical_index
            }))

    return configuration


def make_replication_configuration(key: str, replication_config: Dict, options: Dict=None) -> Dict:
    if replication_config.get('master', None) is None:
        raise RequireMasterConfigException()

    configuration = {}
    configuration[key] = _generate_database_config(
        database_url=replication_config['master'], **(options or {})
    )

    slaves = replication_config.get('slaves', [])
    for index, database_url in enumerate(slaves):
        slave_key = '%s_slave_%d' % (key, index)
        configuration[slave_key] = _generate_database_config(database_url=database_url, is_replica_of=key)

    return configuration


def _generate_database_config(
        database_url: str, is_replica_of: Optional[str]=None, shard_group: Optional[str]=None, shard_number: Optional[int]=None
) -> Dict:
    db_config = config(default=database_url)

    if is_replica_of:
        db_config[DATABASE_CONFIG_MASTER] = is_replica_of

    if shard_group is not None and shard_number is not None:
        db_config[DATABASE_CONFIG_SHARD_GROUP] = shard_group
        db_config[DATABASE_CONFIG_SHARD_NUMBER] = shard_number

    return db_config


def _get_logical_count_per_shard(logical_count: int, shard_count: int) -> int:
    return int(logical_count / shard_count)


def _get_logical_range(shard_index: int, logical_count_per_shard: int) -> Tuple[int, int]:
    start = shard_index * logical_count_per_shard
    end = (shard_index + 1) * logical_count_per_shard

    return start, end


def _make_shard_database_url(origin: str, database_name: str, logical_index: int) -> str:
    if origin == 'sqlite://:memory:':
        return origin

    database_name = '%s_%d' % (database_name, logical_index)
    database_url = '%s%s' % (origin, database_name)

    return database_url


def _make_shard_name(shard_group: str, shard_index: int, logical_index: int) -> str:
    return '%s_%d_%d' % (shard_group, shard_index, logical_index)
