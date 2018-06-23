import os
import sys
from multiprocessing.pool import Pool

from django.core.management.base import BaseCommand

from shard.utils.database import get_master_databases_by_shard_group


class ExecuteQueryOnAllShardCommand(BaseCommand):
    title = 'Execute the query on all shard.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--sql_file', '-f',
            type=str,
            dest='sql_file',
            help='Path of file containing the query',
        )

        parser.add_argument(
            '--shard_group', '-s',
            type=str,
            dest='shard_group',
            help='Shard group to execute',
        )

        parser.add_argument(
            '--manage_file',
            type=str,
            default='manage.py',
            dest='manage_file',
            help='Path of django manage file',
        )

        parser.add_argument(
            '--print_sql',
            action='store_true',
            dest='print_sql',
            help='Print sql before execution',
        )

    @staticmethod
    def assert_if_params_are_not_valid(**options):
        if not options['sql_file']:
            raise Exception('Parameter sql_file is required')

        if not options['shard_group']:
            raise Exception('Parameter shard_group is required')

    def handle(self, *args, **options):
        self.assert_if_params_are_not_valid(**options)

        shard_group = options['shard_group']
        databases = get_master_databases_by_shard_group(shard_group)

        def run_process(shard: str):
            os.system(f'{sys.executable} {options["manage_file"]} execute_query_command -s {shard} -f {options["sql_file"]} --print_sql')

        pool = Pool(processes=len(databases))
        pool.map(run_process, databases)
