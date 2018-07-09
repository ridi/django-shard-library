from django.core.management.base import BaseCommand
from pprint import pprint

from shard.utils.shard import get_shard_by_shard_key_and_shard_group


class Command(BaseCommand):
    title = 'Get shard by key and group'

    def add_arguments(self, parser):
        parser.add_argument(
            '--shard_group', '-s',
            type=str,
            dest='shard_group',
            help='Shard group',
        )

        parser.add_argument(
            '--shard_key', '-k',
            type=str,
            dest='shard key',
            help='Shard Key',
        )

    @staticmethod
    def assert_if_params_are_not_valid(**options):
        if not options['shard_group']:
            raise Exception('Parameter shard_group is required')

        if not options['shard_key']:
            raise Exception('Parameter shard_key is required')

    def handle(self, *args, **options):
        self.assert_if_params_are_not_valid(**options)

        shard = options['shard_group']
        key = options['shard_key']

        pprint(get_shard_by_shard_key_and_shard_group(key, shard))
