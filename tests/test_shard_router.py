from django_dynamic_fixture import G

from shard.routers.shard import ShardRouter
from tests.base import BaseTestCase
from tests.models import ShardModelA, NormalModel, ShardModelB


class ShardRouterTestCase(BaseTestCase):
    def setUp(self):
        self.router = ShardRouter()

    def test_db_for_write_with_shard_object(self):
        obj1 = G(ShardModelA, user_id=1)
        obj2 = G(ShardModelA, user_id=2)
        obj3 = G(ShardModelA, user_id=3)

        write_db1 = self.router.db_for_write(model=obj1.__class__, instance=obj1)
        write_db2 = self.router.db_for_write(model=obj2.__class__, instance=obj2)
        write_db3 = self.router.db_for_write(model=obj3.__class__, instance=obj3)

        self.assertEqual(write_db2, write_db3)
        self.assertNotEqual(write_db1, write_db2)
        self.assertNotEqual(write_db1, write_db3)

    def test_db_for_write_with_normal_object(self):
        obj1 = G(NormalModel, normal_parent=None, shard_parent=None, static_all=None)
        write_db1 = self.router.db_for_write(model=obj1.__class__, hints={'instance': obj1})

        self.assertIsNone(write_db1)

    def test_allow_relations_with_two_shard_objects(self):
        shard_a_obj1 = G(ShardModelA, user_id=1)
        shard_a_obj2 = G(ShardModelA, user_id=2)
        shard_a_obj3 = G(ShardModelA, user_id=3)

        shard_b_obj1 = G(ShardModelB, user_id=1)

        self.assertNotEqual(shard_a_obj1.shard_group, shard_b_obj1.shard_group)

        self.assertTrue(self.router.allow_relation(shard_a_obj2, shard_a_obj3))
        self.assertFalse(self.router.allow_relation(shard_a_obj1, shard_a_obj2))
        self.assertFalse(self.router.allow_relation(shard_a_obj1, shard_a_obj3))

        self.assertFalse(self.router.allow_relation(shard_a_obj1, shard_b_obj1))
        self.assertFalse(self.router.allow_relation(shard_a_obj2, shard_b_obj1))
        self.assertFalse(self.router.allow_relation(shard_a_obj3, shard_b_obj1))
