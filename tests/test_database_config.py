from shard.config.database_config import make_replication_configuration, make_shard_configuration
from shard.constants import DATABASE_CONFIG_MASTER, DATABASE_CONFIG_SHARD_GROUP, DATABASE_CONFIG_SHARD_NUMBER
from tests.base import BaseTestCase


class DatabaseConfigTestCase(BaseTestCase):
    def test_replication_configuration(self):
        defaults_config = make_replication_configuration(
            key='defaults', master={'url': 'mysql://user:pwd@host/metadata'}, slaves=[{'url': 'mysql://user:pwd@host/metadata'}],
            conn_max_age=0
        )
        write_config = make_replication_configuration(
            key='write', master={'url': 'mysql://user:pwd@host/metadata'}, slaves=[], conn_max_age=0
        )

        self.assertEqual(len(defaults_config), 2)
        self.assertEqual(len(write_config), 1)

        self.assertIsNone(write_config['write'].get(DATABASE_CONFIG_MASTER, None))
        self.assertIsNone(defaults_config['defaults'].get(DATABASE_CONFIG_MASTER, None))
        self.assertEqual(defaults_config['defaults_slave_0'][DATABASE_CONFIG_MASTER], 'defaults')

    def test_shard_configuration_only_master(self):
        configs = make_shard_configuration(
            shard_group='GROUP',
            database_name='prepare_product',
            logical_count=4,
            conn_max_age=0,
            options={},
            shards=[{'master': {'url': 'mysql://user:pwd@host/'}}]
        )

        self.assertEqual(len(configs), 4)

        for value in configs.values():
            self.assertEqual(value[DATABASE_CONFIG_SHARD_GROUP], 'GROUP')
            self.assertTrue(DATABASE_CONFIG_SHARD_NUMBER in value)
            self.assertFalse(DATABASE_CONFIG_MASTER in value)

    def test_shard_configuration_with_slave(self):
        configs = make_shard_configuration(
            shard_group='GROUP',
            database_name='prepare_product',
            logical_count=4,
            conn_max_age=0,
            options={},
            shards=[
                {
                    'master': {'url': 'mysql://user:pwd@host/'},
                    'slaves': [{'url': 'mysql://user:pwd@host/'}, {'url': 'mysql://user:pwd@host/'}, ]
                }, {
                    'master': {'url': 'mysql://user:pwd@host/'},
                    'slaves': [{'url': 'mysql://user:pwd@host/'}, {'url': 'mysql://user:pwd@host/'}, ]
                }
            ]
        )

        primary_config = [key for key in configs if configs[key].get(DATABASE_CONFIG_MASTER, None) is None]
        slave_config = {}
        for key in configs:
            if key in primary_config:
                continue

            primary = configs[key]['MASTER']
            if primary not in slave_config:
                slave_config[primary] = []

            slave_config[primary].append(key)

        self.assertEqual(len(primary_config), 4)

        for key in primary_config:
            self.assertEqual(len(slave_config[key]), 2)

            self.assertEqual(configs[key][DATABASE_CONFIG_SHARD_GROUP], 'GROUP')
            self.assertTrue(DATABASE_CONFIG_SHARD_NUMBER in configs[key])

            for slave_key in slave_config[key]:
                self.assertEqual(configs[slave_key][DATABASE_CONFIG_MASTER], key)
