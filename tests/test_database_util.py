# flake8: noqa: E1123  # pylint:disable=unexpected-keyword-arg
from unittest.mock import MagicMock, patch

from django.test import TestCase

from shard.config.helper import ConfigHelper
from shard.utils import database

mock = MagicMock(return_value=ConfigHelper.database_configs(
    unshard={
        'default': {
            'master': 'mysql://user:pwd@host/metadata',
            'slaves': ['mysql://user:pwd@host/metadata', ]
        },
    },
    shard={
        'PRODUCT_GROUP': {
            'shard_options': {
                'database_name': 'product',
                'logical_count': 4,
            },
            'shards': [
                {
                    'master': 'mysql://user:pwd@host/',
                    'slaves': ['mysql://user:pwd@host/', 'mysql://user:pwd@host/', ]
                },
                {
                    'master': 'mysql://user:pwd@host/',
                    'slaves': ['mysql://user:pwd@host/', 'mysql://user:pwd@host/', ]
                }
            ],
        },
        'PREPARE_PRODUCT_GROUP': {
            'shard_options': {
                'database_name': 'prepare_product',
                'logical_count': 2,
            },
            'shards': [
                {
                    'master': 'mysql://user:pwd@host/',
                    'slaves': ['mysql://user:pwd@host/', 'mysql://user:pwd@host/', ]
                },
            ],
        },
    }
))


@patch('shard.utils.database._get_databases', mock)
class DatabaseUtilTestCase(TestCase):
    def test_get_master_databases(self):
        primary_configs_without_shard = database.get_master_databases(without_shard=True, clear=True)
        primary_configs_include_shard = database.get_master_databases(without_shard=False, clear=True)

        self.assertEqual(len(primary_configs_without_shard), 1)
        self.assertEqual(len(primary_configs_include_shard), 7)

    def test_get_master_databases_by_shard_group(self):
        primary_configs_product_group = database.get_master_databases_by_shard_group(shard_group='PRODUCT_GROUP', clear=True)
        primary_configs_prepare_product_group = database.get_master_databases_by_shard_group(
            shard_group='PREPARE_PRODUCT_GROUP', clear=True
        )

        self.assertEqual(len(primary_configs_product_group), 4)
        self.assertEqual(len(primary_configs_prepare_product_group), 2)

    def test_get_slave_databases_by_master(self):
        slave_configs = database.get_slave_databases_by_master(master='default', clear=True)

        self.assertEqual(len(slave_configs), 1)
