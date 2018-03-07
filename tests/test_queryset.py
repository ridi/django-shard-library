from django.db import models
from django.test import TestCase

from django_fake_model import models as f

from shard.mixins import ShardMixin
from shard.exceptions import RequireShardKeyException
from shard.managers import ShardManager
from shard.utils.shard import get_shard_by_shard_key_and_shard_group


class FakeModel(f.FakeModel, ShardMixin):
    user_id = models.IntegerField(verbose_name='유저 idx')

    objects = ShardManager()

    shard_group = 'product_shard'
    shard_key_name = 'user_id'


@FakeModel.fake_me
class QuerysetTestCase(TestCase):
    def setUp(self):
        self.shard_group = 'product_shard'

    def test_quertset(self):
        qs_one = FakeModel.objects.filter(user_id=1)
        qs_two = FakeModel.objects.filter(user_id=2)
        self.assertEqual(get_shard_by_shard_key_and_shard_group(shard_key=1, shard_group=self.shard_group), qs_one.db)
        self.assertEqual(get_shard_by_shard_key_and_shard_group(shard_key=2, shard_group=self.shard_group), qs_two.db)

        fix_shard = FakeModel.objects.shard(shard_key=100)
        self.assertEqual(get_shard_by_shard_key_and_shard_group(shard_key=100, shard_group=self.shard_group), fix_shard.db)

        with self.assertRaises(RequireShardKeyException):
            print(FakeModel.objects.filter())
