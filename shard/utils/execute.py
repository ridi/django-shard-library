from django.db import connections, transaction

from shard.exceptions import QueryExecuteFailureException
from shard.utils.database import get_master_databases_by_shard_group


class QueryExecutor:
    """
    해당 클래스는 DDL 같은 Master 샤드들에 일괄적으로 실행될 필요가 있는 쿼리들을 실행하는 유틸입니다.
    """
    def __init__(self, shard_group: str):
        self._shard_group = shard_group
        self._shards = get_master_databases_by_shard_group(shard_group=shard_group)

    def run_query(self, query: str):
        executed = []
        try:
            for shard in self._shards:
                with transaction.atomic(shard):
                    cursor = connections[shard].cursor()
                    cursor.execute(query)
                executed.append(shard)
        except Exception as e:
            raise QueryExecuteFailureException(shard_group=self._shard_group, executed=executed, exception=e)

        return executed

    def get_shards(self):
        return self._shards
