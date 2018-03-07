
from django.test import TestCase
from unittest.mock import patch

from shard.strategy.routing.random import RandomReadStrategy


def mock_get_slave_databases(master):
    mock_data = {
        'default': ['default_slave_0', 'default_slave_1'],
        'write': [],
    }

    return mock_data.get(master, [])


@patch('shard.strategy.routing.random.RandomReadStrategy.get_slave_databases', mock_get_slave_databases)
class RandomRoutingTestCase(TestCase):
    def setUp(self):
        self.strategy = RandomReadStrategy()

    def test_random_strategy(self):
        self.assertEqual(self.strategy.pick_read_db(master='write'), 'write')
        self.assertNotEqual(self.strategy.pick_read_db(master='default'), 'default')
