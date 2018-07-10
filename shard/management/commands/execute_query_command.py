from django.core.management.base import BaseCommand
from pprint import pprint
from typing import List

from shard.services.execute_query_service import ExecuteQueryService
from shard.services.query_file_handler import QueryFileHandler


class Command(BaseCommand):
    title = 'Execute the query on a shard.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--shard', '-s',
            type=str,
            dest='shard',
            help='Shard to execute the query',
            required=True,
        )

        parser.add_argument(
            '--sql_file', '-f',
            type=str,
            dest='sql_file',
            help='Path of file containing the query',
            required=True,
        )

        parser.add_argument(
            '--transaction', '-t',
            action='store_true',
            dest='with_transaction',
            help='Execute with transaction',
        )

    @staticmethod
    def print_queries(queries: List[str]):
        for query in queries:
            print(query)

    def handle(self, *args, **options):
        shard = options['shard']
        queries = QueryFileHandler.load_queries(options['sql_file'])

        self.print_queries(queries)

        if options['with_transaction']:
            result = ExecuteQueryService.execute_queries_by_shard_with_transaction(shard, queries)
        else:
            result = ExecuteQueryService.execute_queries_by_shard(shard, queries)

        result = {
            'shard': shard,
            'result': result
        }

        pprint(result)
