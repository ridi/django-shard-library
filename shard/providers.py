from shard.exceptions import NotFoundPoolException
from shard.utils.consistent_hash.pool import ConHashPool
from shard.utils.database import get_shard_groups, get_master_databases_by_shard_group, get_tables
from shard.utils.replica import get_replica_count


class PoolProvider:
    def __init__(self):
        self._pools = {}

    def create(self):
        shard_groups = get_shard_groups()

        for shard_group in shard_groups:
            databases = get_master_databases_by_shard_group(shard_group=shard_group)
            tables = get_tables(databases)
            self._pools[shard_group] = ConHashPool(nodes=tables, replica=get_replica_count(shard_group=shard_group))

    def get_pools(self, shard_group: str) -> ConHashPool:
        pool = self._pools.get(shard_group, None)
        if pool is None:
            raise NotFoundPoolException

        return pool

    def get_shard_index(self, shard_group: str, shard_key: int) -> int:
        pool = self.get_pools(shard_group=shard_group)
        return pool.get_node(value=shard_key).index


pool_provider = PoolProvider()
