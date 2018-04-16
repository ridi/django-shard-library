# flake8: noqa: E1123  # pylint:disable=unexpected-keyword-arg
# flake8: noqa: W0212 pylint: disable=protected-access
from django.test import TestCase
from django_dynamic_fixture import G

from shard.constants import DEFAULT_DATABASE
from shard.utils.database import get_master_databases_by_shard_group, get_master_databases_for_shard
from shard_static.exceptions import InvalidDatabaseAliasException, NotShardStaticException
from shard_static.services import sync_static_service
from tests.models import ShardStaticA, ShardStaticAll, ShardStaticB


class SyncStaticServiceTestCase(TestCase):
    # 같은 shard_group의 db가 아닐때

    def test_sync_success_with_shard_a_only(self):
        _objs = [G(ShardStaticA) for _ in range(10)]
        databases = get_master_databases_by_shard_group(shard_group=ShardStaticA.shard_group, clear=True)

        try:
            for db in databases:
                sync_static_service.sync_static('tests.ShardStaticA', db)
        except:  # flake8: noqa: E722  # pylint:disable=bare-except
            self.fail('sync_static is fail')

        for db in databases:
            self.assertEqual(len(_objs), ShardStaticA.objects.shard(shard=db).count())

        # Clear Database For isolating testcase
        for db in databases:
            ShardStaticA.objects.shard(shard=db).delete()

    def test_sync_success_with_shard_all(self):
        _objs = [G(ShardStaticAll) for _ in range(10)]
        databases = get_master_databases_for_shard(clear=True)

        try:
            for db in databases:
                sync_static_service.sync_static('tests.ShardStaticAll', db)
        except:  # flake8: noqa: E722  # pylint:disable=bare-except
            self.fail('sync_static is fail')

        for db in databases:
            self.assertEqual(len(_objs), ShardStaticAll.objects.shard(shard=db).count())

        # Clear Database For isolating testcase
        for db in databases:
            ShardStaticAll.objects.shard(shard=db).delete()

    def test_sync_failure_with_invalid_database_alias(self):
        with self.assertRaises(InvalidDatabaseAliasException):
            sync_static_service.sync_static('tests.ShardStaticAll', DEFAULT_DATABASE)

    def test_sync_failure_with_different_between_object_and_shard_group(self):
        databases = get_master_databases_by_shard_group(shard_group=ShardStaticB.shard_group, clear=True)

        with self.assertRaises(InvalidDatabaseAliasException):
            for db in databases:
                sync_static_service.sync_static('tests.ShardStaticA', db)

    def test_sync_failure_with_normal_model(self):
        database = get_master_databases_by_shard_group(shard_group=ShardStaticB.shard_group, clear=True)[0]

        with self.assertRaises(NotShardStaticException):
            sync_static_service.sync_static('tests.NormalModel', database)