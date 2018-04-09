import django
import sys

from django.conf import settings
from django.test.utils import get_runner

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
            'product_shard': {
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
        'shard_static',
    ],
    'DATABASE_ROUTERS': [
        'shard.routers.specific.SpecificRouter', 'shard.routers.shard.ShardRouter',
    ]
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
