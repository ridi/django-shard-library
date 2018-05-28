import django
import sys

from django.conf import settings
from django.test.utils import get_runner

from shard.config.helper import ConfigHelper

SETTINGS_DICT = {
    'DEBUG': True,
    'USE_TZ': True,
    'DATABASES': ConfigHelper.generate_database_configs(
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
        'shard',
        'shard_static',
    ],
    'DATABASE_ROUTERS': ['shard.routers.specific.SpecificRouter', 'shard_static.routers.ShardStaticRouter'],
    'SHARD_TRANSMIT_LOCK_MANAGER_CLASS': 'tests.lock.FakeLockManager',
}


def run_tests(*test_args):
    settings.configure(**SETTINGS_DICT)
    django.setup()

    if not test_args:
        test_args = ['tests']

    # Run tests
    TestRunner = get_runner(settings)
    test_runner = TestRunner()

    failures = test_runner.run_tests(test_args, interactive=False)

    if failures:
        sys.exit(bool(failures))

    sys.exit(0)


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
