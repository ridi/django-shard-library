import sys

import django
from django.conf import settings

from shard.config.helper import ConfigHelper

SETTINGS_DICT = {
    'DEBUG': True,
    'USE_TZ': True,
    'DATABASES': ConfigHelper.database_configs(
        unshard={
            'default': {
                'master': 'sqlite://:memory:',
            },
        },
        shard={
            'shard_a': {
                'shard_options': {
                    'database_name': 'product',
                    'logical_count': 2,
                },
                'shards': [
                    {
                        'master': 'sqlite://:memory:',
                    },
                    {
                        'master': 'sqlite://:memory:',
                    },
                ]
            },
            'shard_b': {
                'shard_options': {
                    'database_name': 'product',
                    'logical_count': 2,
                },
                'shards': [
                    {
                        'master': 'sqlite://:memory:',
                    },
                    {
                        'master': 'sqlite://:memory:',
                    },
                ]
            }
        }
    ),
    'INSTALLED_APPS': [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sites',
        'tests',
        'shard_static_sync',
    ],
    'DATABASE_ROUTERS': [
        'shard.routers.specific.SpecificRouter', 'shard.routers.shard.ShardRouter',
    ]
}


def run_command(*args):
    settings.configure(**SETTINGS_DICT)
    django.setup()

    from django.core.management import execute_from_command_line
    execute_from_command_line(args)


if __name__ == '__main__':
    run_command(*sys.argv[:])
