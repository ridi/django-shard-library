import copy
import urllib.parse
from typing import Dict, List, Optional, Tuple

from dj_database_url import config

from shard.constants import DATABASE_CONFIG_MASTER, DATABASE_CONFIG_SHARD_GROUP, DATABASE_CONFIG_SHARD_NUMBER

__all__ = ('make_shard_configuration', 'make_replication_configuration', )


def make_shard_configuration(
        shard_group: str, database_name: str, logical_count: int, conn_max_age: int, shards: List, options: Dict
) -> Dict:
    configuration = {}
    shard_count = len(shards)
    logical_count_per_shard = _get_logical_count_per_shard(logical_count=logical_count, shard_count=shard_count)

    for index, shard in enumerate(shards):
        master_shard = shard['master']
        slave_shards = shard.get('slaves', [])

        start, end = _get_logical_range(index, logical_count_per_shard)
        for logical_index in range(start, end):
            shard_name = _make_shard_name(shard_group=shard_group, shard_count=shard_count, shard_index=index, logical_index=logical_index)

            _master_shard, _slave_shards = _make_shard_config(master_shard, slave_shards, database_name, logical_index, options)
            configuration.update(make_replication_configuration(
                key=shard_name, master=_master_shard, slaves=_slave_shards, conn_max_age=conn_max_age, shard_info={
                    'shard_group': shard_group, 'shard_number': logical_index}
            ))

    return configuration


def make_replication_configuration(key: str, master: Dict, slaves: List[Dict], conn_max_age: int, shard_info: Optional[Dict]=None) -> Dict:
    configuration = {}

    if shard_info is None:
        shard_info = {}

    configuration[key] = _generate_database_config(
        database_url=master['url'], conn_max_age=master.get('conn_max_age', conn_max_age), **shard_info
    )

    for index, slave in enumerate(slaves):
        slave_key = '%s_slave_%d' % (key, index)
        configuration[slave_key] = _generate_database_config(
            database_url=slave['url'], conn_max_age=slave.get('conn_max_age', conn_max_age), is_replica_of=key
        )

    return configuration


def _make_shard_config(master_shard: Dict, slave_shards: List, database_name: str, logical_index: int, options: Dict) -> Tuple[Dict, List]:
    _master_shard = copy.deepcopy(master_shard)
    _master_shard.update({
        'url': _make_shard_database_url(
            origin=master_shard['url'], database_name=database_name, logical_index=logical_index,
            db_options={**options, **(_master_shard.get('options', {}))}
        ),
    })

    _slave_shards = copy.deepcopy(slave_shards)
    for slave_shard in _slave_shards:
        slave_shard.update({
            'url': _make_shard_database_url(
                origin=slave_shard['url'], database_name=database_name, logical_index=logical_index,
                db_options={**options, **(slave_shard.get('options', {}))}
            )
        })

    return _master_shard, _slave_shards


def _generate_database_config(
        database_url: str, conn_max_age: int, is_replica_of: Optional[str]=None, shard_group: Optional[str]=None,
        shard_number: Optional[int]=None
) -> Dict:
    db_config = config(default=database_url, conn_max_age=conn_max_age)

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


def _make_shard_database_url(origin: str, database_name: str, logical_index: int, db_options: Optional[Dict]=None) -> str:
    if origin == 'sqlite://:memory:':
        return origin

    database_name = '%s_%d' % (database_name, logical_index)
    database_url = '%s%s' % (origin, database_name)

    if db_options:
        database_url = database_url + '?' + urllib.parse.urlencode(db_options)

    return database_url


def _make_shard_name(shard_group: str, shard_count: int, shard_index: int, logical_index: int) -> str:
    return '%s_%d_%d_%d' % (shard_group, shard_count, shard_index, logical_index)
