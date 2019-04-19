from shard.utils.memorize import memorize
from tests.base import BaseTestCase


def dummy_func(value):
    return object()


class MemorizeUtilTestCase(BaseTestCase):
    def setUp(self):
        self.func = memorize(dummy_func)

    def test_memorize(self):
        obj = self.func(value=1)
        obj2 = self.func(value=1)

        self.assertEqual(id(obj), id(obj2))

    def test_memorize_another_key(self):
        obj = self.func(value=1)
        obj2 = self.func(value=1)
        obj3 = self.func(value=2)

        self.assertEqual(id(obj), id(obj2))
        self.assertNotEqual(id(obj), id(obj3))
        self.assertNotEqual(id(obj2), id(obj3))

    def test_memorize_clear(self):
        obj = self.func(value=1, clear=True)
        obj2 = self.func(value=1, clear=True)

        self.assertNotEqual(id(obj), id(obj2))
