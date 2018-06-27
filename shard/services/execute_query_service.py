from django.db import DatabaseError, connections, transaction
from typing import Dict, List


class ExecuteQueryService:
    @classmethod
    def execute_queries_by_shard(cls, shard: str, queries: List[str]) -> List:
        with connections[shard].cursor() as cursor:
            return cls.execute_queries(cursor, queries)

    @classmethod
    def execute_queries_by_shard_with_transaction(cls, shard: str, queries: List[str]) -> List:
        with transaction.atomic(shard):
            with connections[shard].cursor() as cursor:
                return cls.execute_queries(cursor, queries)

    @classmethod
    def execute_queries(cls, cursor, queries: List[str]) -> List:
        result = []
        for query in queries:
            result.append(cls.execute_query(cursor, query))

        return result

    @classmethod
    def execute_query(cls, cursor, query: str) -> Dict:
        result = {
            'query': query
        }

        try:
            result['result'] = cursor.execute(query)

        except DatabaseError as e:
            result['error'] = str(e)

        if cursor.description:
            result['items'] = cls._parse_result(cursor)

        return result

    @staticmethod
    def _parse_result(cursor):
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
