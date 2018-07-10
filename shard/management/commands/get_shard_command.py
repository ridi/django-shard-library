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
            required=True,
        )

        parser.add_argument(
            '--shard_key', '-k',
            type=str,
            dest='shard_key',
            help='Shard Key',
            required=True,
        )

    def handle(self, *args, **options):
        pprint(get_shard_by_shard_key_and_shard_group(options['shard_key'], options['shard_group']))
