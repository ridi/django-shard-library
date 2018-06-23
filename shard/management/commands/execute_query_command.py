from django.core.management.base import BaseCommand
from django.db import DatabaseError, connections


class ExecuteQueryCommand(BaseCommand):
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

        if not options['shard']:
            raise Exception('Parameter shard is required')

    def handle(self, *args, **options):
        self.assert_if_params_are_not_valid(**options)

        shard = options['shard']
        queries = self._load_queries(options['sql_file'])

        self._log(shard)

        with connections[shard].cursor() as cursor:
            for query in queries:
                if not query:
                    continue

                if options['print_sql']:
                    self._log(query)

                try:
                    result = cursor.execute(query)
                    self._log(str(result))

                except DatabaseError as e:
                    self._log(str(e))
                    return

                if cursor.description:
                    self._log(str(self.parse_result(cursor)))

    @staticmethod
    def parse_result(cursor):
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    @staticmethod
    def _load_queries(file_name: str):
        file = open(file_name, 'r')
        query = file.read()
        file.close()

        query_list = [s and s.strip() for s in query.split(';')]
        return list(filter(None, query_list))

    @staticmethod
    def _log(log_message: str):
        print(log_message)
