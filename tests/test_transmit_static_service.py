# flake8: noqa: E1123  # pylint:disable=unexpected-keyword-arg
# flake8: noqa: W0212 pylint: disable=protected-access
from django.test import TestCase
from django_dynamic_fixture import G

from shard.utils.database import get_master_databases_by_shard_group
from shard_static.exceptions import InvalidDatabaseAliasException, NotShardStaticException
from shard_static.services import static_transmit_service
from tests.models import ShardStaticA, ShardStaticB


class TransmitStaticServiceTestCase(TestCase):
    def test_transmit_success(self):
        _objs = [G(ShardStaticA) for _ in range(10)]
        databases = get_master_databases_by_shard_group(shard_group=ShardStaticA.shard_group, clear=True)

        for db in databases:
            static_transmit_service.run_transmit_with_lock('tests.ShardStaticA', db)
            self.assertEqual(len(_objs), ShardStaticA.objects.shard(shard=db).count())

        # Clear Database For isolating testcase
        for db in databases:
            ShardStaticA.objects.shard(shard=db).delete()

    def test_transmit_success_when_update(self):
        _objs = [G(ShardStaticA) for _ in range(10)]
        databases = get_master_databases_by_shard_group(shard_group=ShardStaticA.shard_group, clear=True)

        for db in databases:
            static_transmit_service.run_transmit_with_lock('tests.ShardStaticA', db)
            self.assertEqual(len(_objs), ShardStaticA.objects.shard(shard=db).count())

        obj = _objs[0]
        obj.text = 'for test'
        obj.save()

        for db in databases:
            static_transmit_service.run_transmit_with_lock('tests.ShardStaticA', db)
            updated = ShardStaticA.objects.shard(shard=db).get(id=obj.id).text
            self.assertEqual(updated, 'for test')

        # Clear Database For isolating testcase
        for db in databases:
            ShardStaticA.objects.shard(shard=db).delete()

    def test_transmit_failure_with_different_between_object_and_shard_group(self):
        databases = get_master_databases_by_shard_group(shard_group=ShardStaticB.shard_group, clear=True)

        with self.assertRaises(InvalidDatabaseAliasException):
            for db in databases:
                static_transmit_service.run_transmit_with_lock('tests.ShardStaticA', db)

    def test_transmit_failure_with_normal_model(self):
        database = get_master_databases_by_shard_group(shard_group=ShardStaticB.shard_group, clear=True)[0]

        with self.assertRaises(NotShardStaticException):
            static_transmit_service.run_transmit_with_lock('tests.NormalModel', database)
