from django.test import TestCase

from shard_static.constants import DEFAULT_LOCK_TTL
from tests.lock import FakeLockManager


class LockTestCase(TestCase):
    def setUp(self):
        self.lock_manager_one = FakeLockManager(key='test-key')
        self.lock_manager_two = FakeLockManager(key='test-key')

        # clear fake lock_manager
        self.lock_manager_one.release()

    def test_set_key_and_ttl(self):
        lock1 = FakeLockManager(key='tk-one')
        lock2 = FakeLockManager(key='tk-two', ttl=60 * 10)

        self.assertEqual(lock1.key, 'tk-one')
        self.assertEqual(lock1.ttl, DEFAULT_LOCK_TTL)

        self.assertEqual(lock2.key, 'tk-two')
        self.assertEqual(lock2.ttl, 60 * 10)

    def test_lock(self):
        self.assertTrue(self.lock_manager_one.lock())
        self.assertFalse(self.lock_manager_one.lock())

    def test_release(self):
        self.assertFalse(self.lock_manager_one.release())

        self.assertTrue(self.lock_manager_one.lock())

        self.assertTrue(self.lock_manager_one.release())

    def test_is_locked(self):
        self.assertTrue(self.lock_manager_one.lock())

        self.assertTrue(self.lock_manager_one.is_locked())
        self.assertTrue(self.lock_manager_two.is_locked())

        self.assertTrue(self.lock_manager_one.release())

        self.assertFalse(self.lock_manager_one.is_locked())
        self.assertFalse(self.lock_manager_two.is_locked())

    def test_ping(self):
        self.assertFalse(self.lock_manager_one.ping())
        self.assertFalse(self.lock_manager_two.ping())

        self.assertTrue(self.lock_manager_one.lock())

        self.assertTrue(self.lock_manager_one.ping())
        self.assertTrue(self.lock_manager_two.ping())
