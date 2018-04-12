from django.test import TestCase

from shard.exceptions import RequireShardKeyException
from shard.utils.shard import get_shard_by_shard_key_and_shard_group
from tests.models import ShardModelA


class QuerysetTestCase(TestCase):
    def setUp(self):
        self.shard_group = 'shard_a'

    def test_filter(self):
        qs_one = ShardModelA.objects.filter(user_id=1)
        qs_two = ShardModelA.objects.filter(user_id=2)
        self.assertEqual(get_shard_by_shard_key_and_shard_group(shard_key=1, shard_group=self.shard_group), qs_one.db)
        self.assertEqual(get_shard_by_shard_key_and_shard_group(shard_key=2, shard_group=self.shard_group), qs_two.db)

        fix_shard = ShardModelA.objects.filter(user_id=100)
        self.assertEqual(get_shard_by_shard_key_and_shard_group(shard_key=100, shard_group=self.shard_group), fix_shard.db)

        with self.assertRaises(RequireShardKeyException):
            ShardModelA.objects.filter()

    def test_get(self):
        with self.assertRaises(RequireShardKeyException):
            ShardModelA.objects.get()

        with self.assertRaises(ShardModelA.DoesNotExist):
            ShardModelA.objects.get(user_id=1)

        try:
            ShardModelA.objects.create(user_id=1)
            obj = ShardModelA.objects.get(user_id=1)
            obj.delete()
        except:
            self.fail('ShardQuerySet get method is not normally.')

    def test_create(self):
        with self.assertRaises(RequireShardKeyException):
            ShardModelA.objects.create()

        try:
            obj = ShardModelA.objects.create(user_id=3)
            obj.delete()
        except:
            self.fail('ShardQuerySet create method is not normally.')

    def test_get_or_create(self):
        with self.assertRaises(RequireShardKeyException):
            ShardModelA.objects.get_or_create()

        try:
            obj, created = ShardModelA.objects.get_or_create(user_id=4)
            obj_late, created_late = ShardModelA.objects.get_or_create(user_id=4)

            self.assertEqual(obj.id, obj_late.id)
            self.assertEqual(obj._state.db, obj_late._state.db)
            self.assertTrue(created)
            self.assertFalse(created_late)

            obj.delete()
        except:
            self.fail('ShardQuerySet get_or_create method is not normally.')

    def test_update_or_create(self):
        with self.assertRaises(RequireShardKeyException):
            ShardModelA.objects.update_or_create()

        try:
            obj, created = ShardModelA.objects.update_or_create(user_id=3, defaults={'text': 'This is Text One'})
            self.assertEqual(obj.text, 'This is Text One')
            self.assertTrue(created)

            obj, created = ShardModelA.objects.update_or_create(user_id=3, defaults={'text': 'This is Text Two'})
            self.assertEqual(obj.text, 'This is Text Two')
            self.assertFalse(created)

            obj.delete()
        except:
            self.fail('ShardQuerySet update_or_create method is not normally.')
