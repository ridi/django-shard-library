# flake8: noqa: E1123  # pylint:disable=unexpected-keyword-arg
from unittest.mock import MagicMock, patch

from shard.config.helper import ConfigHelper
from shard.utils import database
from tests.base import BaseTestCase

mock = MagicMock(return_value=ConfigHelper.generate_database_configs(
    unshard={
        'default': {
            'master': {'url': 'mysql://user:pwd@host/metadata'},
            'slaves': [{'url': 'mysql://user:pwd@host/metadata'}, ]
        },
    },
    shard={
        'PRODUCT_GROUP': {
            'database_name': 'product',
            'logical_count': 4,
            'shards': [
                {
                    'master': {'url': 'mysql://user:pwd@host/'},
                    'slaves': [{'url': 'mysql://user:pwd@host/'}, {'url': 'mysql://user:pwd@host/'}, ]
                },
                {
                    'master': {'url': 'mysql://user:pwd@host/'},
                    'slaves': [{'url': 'mysql://user:pwd@host/'}, {'url': 'mysql://user:pwd@host/'}, ]
                }
            ],
        },
        'PREPARE_PRODUCT_GROUP': {
            'database_name': 'prepare_product',
            'logical_count': 2,
            'shards': [
                {
                    'master': {'url': 'mysql://user:pwd@host/'},
                    'slaves': [{'url': 'mysql://user:pwd@host/'}, {'url': 'mysql://user:pwd@host/'}, ]
                },
            ],
        },
    }
))


class DatabaseUtilTestCase(BaseTestCase):
    @patch('shard.utils.database._get_databases', mock)
    def test_get_master_databases(self):
        primary_configs_without_shard = database.get_master_databases(without_shard=True, nocache=True)
        primary_configs_include_shard = database.get_master_databases(without_shard=False, nocache=True)

        self.assertEqual(len(primary_configs_without_shard), 1)
        self.assertEqual(len(primary_configs_include_shard), 7)

    @patch('shard.utils.database._get_databases', mock)
    def test_get_master_databases_for_shard(self):
        databases = database.get_master_databases_for_shard(clear=True)

        self.assertEqual(len(databases), 6)

    @patch('shard.utils.database._get_databases', mock)
    def test_get_master_databases_by_shard_group(self):
        primary_configs_product_group = database.get_master_databases_by_shard_group(shard_group='PRODUCT_GROUP', nocache=True)
        primary_configs_prepare_product_group = database.get_master_databases_by_shard_group(
            shard_group='PREPARE_PRODUCT_GROUP', nocache=True
        )

        self.assertEqual(len(primary_configs_product_group), 4)
        self.assertEqual(len(primary_configs_prepare_product_group), 2)

    @patch('shard.utils.database._get_databases', mock)
    def test_get_slave_databases_by_master(self):
        slave_configs = database.get_slave_databases_by_master(master='default', nocache=True)

        self.assertEqual(len(slave_configs), 1)
