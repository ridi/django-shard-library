from typing import Dict, List

from django.db import DatabaseError, connections


class ExecuteQueryService:
    @classmethod
    def execute_queries(cls, shard: str, queries: List[str]) -> List:
        result = []
        with connections[shard].cursor() as cursor:
            for query in queries:
                result.append(cls.execute_query(cursor, query))

        return result

    @classmethod
    def execute_query(cls, cursor, query) -> Dict:
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
