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
                'master': 'mysql://root:root@127.0.0.1/default?sql_mode=STRICT_TRANS_TABLES&charset=utf8',
            },
        },
        shard={
            'shard_a': {
                'shard_options': {
                    'database_name': 'shard_a',
                    'logical_count': 2,
                },
                'db_options': {
                    'sql_mode': 'STRICT_TRANS_TABLES',
                    'charset': 'utf8',
                },
                'shards': [
                    {
                        'master': 'mysql://root:root@127.0.0.1/',
                    },
                    {
                        'master': 'mysql://root:root@127.0.0.1/',
                    },
                ]
            },
            'shard_b': {
                'shard_options': {
                    'database_name': 'shard_b',
                    'logical_count': 2,
                },
                'db_options': {
                    'sql_mode': 'STRICT_TRANS_TABLES',
                    'charset': 'utf8',
                },
                'shards': [
                    {
                        'master': 'mysql://root:root@127.0.0.1/',
                    },
                    {
                        'master': 'mysql://root:root@127.0.0.1/',
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
        'shard_static',
    ],
    'DATABASE_ROUTERS': ['shard.routers.specific.SpecificRouter', 'shard_static.routers.ShardStaticRouter'],
    'SHARD_SYNC_LOCK_MANAGER_CLASS': 'tests.lock.FakeLockManager',
}


def run_command(*args):
    settings.configure(**SETTINGS_DICT)
    django.setup()

    from django.core.management import execute_from_command_line
    execute_from_command_line(args)


if __name__ == '__main__':
    run_command(*sys.argv[:])