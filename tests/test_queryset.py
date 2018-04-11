from django.test import TestCase

from shard.exceptions import RequireShardKeyException
from shard.utils.shard import get_shard_by_shard_key_and_shard_group
from tests.models import ShardModelA


class QuerysetTestCase(TestCase):
    def setUp(self):
        self.shard_group = 'shard_a'

    def test_quertset(self):
        qs_one = ShardModelA.objects.filter(user_id=1)
        qs_two = ShardModelA.objects.filter(user_id=2)
        self.assertEqual(get_shard_by_shard_key_and_shard_group(shard_key=1, shard_group=self.shard_group), qs_one.db)
        self.assertEqual(get_shard_by_shard_key_and_shard_group(shard_key=2, shard_group=self.shard_group), qs_two.db)

        fix_shard = ShardModelA.objects.filter(user_id=100)
        self.assertEqual(get_shard_by_shard_key_and_shard_group(shard_key=100, shard_group=self.shard_group), fix_shard.db)

        with self.assertRaises(RequireShardKeyException):
            ShardModelA.objects.filter()
