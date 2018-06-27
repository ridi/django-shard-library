from django.core.management.base import BaseCommand
from multiprocessing.pool import Pool
from pprint import pprint
from typing import Dict

from shard.services.execute_query_service import ExecuteQueryService
from shard.services.query_file_handler import QueryFileHandler
from shard.utils.database import get_master_databases_by_shard_group


def run_process(params) -> Dict:
    if params['with_transaction']:
        result = ExecuteQueryService.execute_queries_by_shard_with_transaction(params['shard'], params['queries'])
    else:
        result = ExecuteQueryService.execute_queries_by_shard(params['shard'], params['queries'])

    return {
        'shard': params['shard'],
        'result': result
    }


class Command(BaseCommand):
    title = 'Execute the query on all shard.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--shard_group', '-s',
            type=str,
            dest='shard_group',
            help='Shard group to execute',
        )

        parser.add_argument(
            '--sql_file', '-f',
            type=str,
            dest='sql_file',
            help='Path of file containing the query',
        )

        parser.add_argument(
            '--transaction', '-t',
            action='store_true',
            dest='with_transaction',
            help='Execute with transaction',
        )

    @staticmethod
    def assert_if_params_are_not_valid(**options):
        if not options['shard_group']:
            raise Exception('Parameter shard_group is required')

        if not options['sql_file']:
            raise Exception('Parameter sql_file is required')

    def handle(self, *args, **options):
        self.assert_if_params_are_not_valid(**options)

        shard_group = options['shard_group']
        databases = get_master_databases_by_shard_group(shard_group)
        queries = QueryFileHandler.load_queries(options['sql_file'])
        params = [
            {'shard': database, 'queries': queries, 'with_transaction': options['with_transaction']} for database in databases
        ]

        pool = Pool(processes=len(databases))
        result = {
            'shard_group': shard_group,
            'result': pool.map(run_process, params),
        }

        pprint(result)
