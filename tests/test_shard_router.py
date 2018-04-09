from django.conf import settings
from django.test import TestCase
from django_dynamic_fixture import G

from shard.routers.shard import ShardRouter
from tests.models import ShardModelA, NormalModel


class ShardRouterTestCase(TestCase):
    '''
    # Allow_relation
        # Two Shard objs (Same group, Other group)
        # a normal model and a shard model
        # One Shard obj and One Shard Static obj (Same group, Other group, all_group)

        # Two Shard Static Objs (Same group and other group and all_group)
        # Not Shard objs (has not opnion)
    '''

    def setUp(self):
        self.router = ShardRouter()

    def test_db_for_write_with_shard_object(self):
        obj1 = G(ShardModelA, user_id=1)
        obj2 = G(ShardModelA, user_id=2)
        obj3 = G(ShardModelA, user_id=3)

        write_db1 = self.router.db_for_write(model=obj1.__class__, instance=obj1)
        write_db2 = self.router.db_for_write(model=obj2.__class__, instance=obj2)
        write_db3 = self.router.db_for_write(model=obj3.__class__, instance=obj3)

        self.assertEqual(write_db1, write_db3)
        self.assertNotEqual(write_db1, write_db2)

    def test_db_for_write_with_normal_object(self):
        obj1 = G(NormalModel)
        write_db1 = self.router.db_for_write(model=obj1.__class__, hints={'instance': obj1})

        self.assertIsNone(write_db1)
