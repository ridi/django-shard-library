from shard.constants import DEFAULT_DATABASE
from shard.mixins import SpecificDatabaseMixin
from shard.routers.specific import SpecificRouter
from tests.base import BaseTestCase


class TestSpecificDefault(SpecificDatabaseMixin):
    _specific_database = DEFAULT_DATABASE


class TestSpecificDummy(SpecificDatabaseMixin):
    _specific_database = 'dummy'


class SpecificRouterTestCase(BaseTestCase):

    def setUp(self):

        self.router = SpecificRouter()
        self.default_object_one = TestSpecificDefault()
        self.default_object_two = TestSpecificDefault()

        self.dummy_object = TestSpecificDummy()

    def test_db_for_read(self):
        db_default_one = self.router.db_for_read(model=self.default_object_one.__class__)
        db_default_two = self.router.db_for_read(model=self.default_object_two.__class__)
        db_dummy = self.router.db_for_read(model=self.dummy_object.__class__)

        self.assertEqual(db_default_one, self.default_object_one.specific_database())
        self.assertEqual(db_default_two, self.default_object_two.specific_database())
        self.assertEqual(db_default_one, db_default_two)

        self.assertEqual(db_dummy, self.dummy_object.specific_database())

    def test_db_for_write(self):
        db_default_one = self.router.db_for_write(model=self.default_object_one.__class__)
        db_default_two = self.router.db_for_write(model=self.default_object_two.__class__)
        db_dummy = self.router.db_for_write(model=self.dummy_object.__class__)

        self.assertEqual(db_default_one, self.default_object_one.specific_database())
        self.assertEqual(db_default_two, self.default_object_two.specific_database())
        self.assertEqual(db_default_one, db_default_two)

        self.assertEqual(db_dummy, self.dummy_object.specific_database())

    def test_db_allow_relation(self):
        is_allow_relation1 = self.router.allow_relation(self.default_object_one, self.default_object_two)
        is_allow_relation2 = self.router.allow_relation(self.default_object_one, self.dummy_object)

        self.assertTrue(is_allow_relation1)
        self.assertFalse(is_allow_relation2)
