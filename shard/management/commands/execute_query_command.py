from django.core.management.base import BaseCommand

from shard.services.execute_query_service import ExecuteQueryService


class Command(BaseCommand):
    title = 'Execute the query on a shard.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--shard', '-s',
            type=str,
            dest='shard',
            help='Shard to execute the query',
        )

        parser.add_argument(
            '--sql_file', '-f',
            type=str,
            dest='sql_file',
            help='Path of file containing the query',
        )

    @staticmethod
    def assert_if_params_are_not_valid(**options):
        if not options['shard']:
            raise Exception('Parameter shard is required')

        if not options['sql_file']:
            raise Exception('Parameter sql_file is required')

    def handle(self, *args, **options):
        self.assert_if_params_are_not_valid(**options)

        shard = options['shard']
        queries = self._load_queries(options['sql_file'])

        result = {
            'shard': shard,
            'result': ExecuteQueryService.execute_queries(shard, queries)
        }

        print(result)

    @staticmethod
    def _load_queries(file_name: str):
        file = open(file_name, 'r')
        query = file.read()
        file.close()

        query_list = [s and s.strip() for s in query.split(';')]
        return list(filter(None, query_list))
