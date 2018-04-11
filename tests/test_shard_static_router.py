from django.test import TestCase
from django_dynamic_fixture import G

from shard.utils.shard import get_shard_by_shard_key_and_shard_group
from shard_static.routers import ShardStaticRouter
from tests.models import ShardModelA, NormalModel, ShardModelB, ShardStaticAll, ShardStaticA, ShardStaticB


class ShardStaticRouterTestCase(TestCase):
    def setUp(self):
        self.router = ShardStaticRouter()

    def test_allow_relation_with_a_shard_object_and_a_static_object(self):
        shard_a_obj1 = G(ShardModelA, user_id=1)
        shard_b_obj1 = G(ShardModelB, user_id=1)

        shard_all_static = G(ShardStaticAll)
        shard_a_static = G(ShardStaticA)

        self.assertTrue(self.router.allow_relation(shard_a_obj1, shard_a_static))
        self.assertFalse(self.router.allow_relation(shard_b_obj1, shard_a_static))

        self.assertTrue(self.router.allow_relation(shard_a_obj1, shard_all_static))
        self.assertTrue(self.router.allow_relation(shard_b_obj1, shard_all_static))

    def test_allow_relation_with_a_normal_object_and_a_static_object(self):
        shard_all_static = G(ShardStaticAll)
        shard_a_static = G(ShardStaticA)
        shard_b_static = ShardStaticB.objects.shard(
            get_shard_by_shard_key_and_shard_group(shard_key=1, shard_group=ShardStaticB.shard_group)
        ).create()

        normal_object = G(NormalModel)

        self.assertTrue(self.router.allow_relation(normal_object, shard_all_static))
        self.assertTrue(self.router.allow_relation(normal_object, shard_a_static))
        self.assertFalse(self.router.allow_relation(normal_object, shard_b_static))

        self.assertFalse(shard_b_static.diffusible)

        # delete instance for isolation test
        shard_b_static.delete()

    def test_allow_relation_with_two_static_objects(self):
        shard_all_static = G(ShardStaticAll)
        shard_a_static = G(ShardStaticA)
        shard_b_static = ShardStaticB.objects.shard(
            get_shard_by_shard_key_and_shard_group(shard_key=1, shard_group=ShardStaticB.shard_group)
        ).create()

        self.assertTrue(self.router.allow_relation(shard_a_static, shard_all_static))
        self.assertTrue(self.router.allow_relation(shard_b_static, shard_all_static))
        self.assertFalse(self.router.allow_relation(shard_a_static, shard_b_static))

        # delete instance for isolation test
        shard_b_static.delete()

    def test_allow_relation_with_two_normal_objects(self):
        normal_object1 = G(NormalModel)
        normal_object2 = G(NormalModel)

        self.assertIsNone(self.router.allow_relation(normal_object1, normal_object2))
