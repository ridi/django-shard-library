from unittest.mock import patch

from django.test import TestCase

from shard_static import config
from shard_static.lock import BaseLockManager
from shard_static.services import lock_service
from tests.lock import FakeLockManager


class LockServiceTestCase(TestCase):
    def setUp(self):
        self.model_name = 'this.is.model'
        self.database_alias = 'test_alias'
        self.lock_manager = lock_service.get_lock_manager(self.model_name, self.database_alias)

    def test_get_lock_manager(self):
        self.assertIsInstance(self.lock_manager, BaseLockManager)
        self.assertIsInstance(self.lock_manager, FakeLockManager)

        self.assertEqual(config.SHARD_SYNC_LOCK_MANAGER_CLASS, FakeLockManager.__module__ + '.' + FakeLockManager.__name__)

    def test_make_key(self):
        self.assertEqual(self.lock_manager.key, lock_service._make_lock_key(self.model_name, self.database_alias))
        self.assertEqual(self.lock_manager.ttl, config.SHARD_SYNC_LOCK_TTL)

    def test_import_lock_manager_class(self):
        lock_manager_class = lock_service._import_lock_manager_class()

        self.assertEqual(lock_manager_class, FakeLockManager)
        self.assertEqual(config.SHARD_SYNC_LOCK_MANAGER_CLASS, lock_manager_class.__module__ + '.' + lock_manager_class.__name__)

    @patch('shard_static.config.SHARD_SYNC_LOCK_MANAGER_CLASS', 'not.exists.package')
    def test_raise_import_error_in_import_lock_manager_class(self):
        with self.assertRaises(ImportError):
            lock_service._import_lock_manager_class()

    @patch('shard_static.config.SHARD_SYNC_LOCK_MANAGER_CLASS', 'tests.lock.NotExistLockManager')
    def test_raise_attribute_error_in_import_lock_manager_class(self):
        with self.assertRaises(AttributeError):
            lock_service._import_lock_manager_class()
