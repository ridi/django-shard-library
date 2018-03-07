from django.test import TestCase

from shard.mixins import SpecificDatabaseMixin
from shard.exceptions import RequireSpecificDatabaseException


class SpecificDatabaseMixinTestCase(TestCase):
    def setUp(self):
        class NotSelectSpecificDatabase(SpecificDatabaseMixin):
            pass

        class SelectSpecificDatabase(SpecificDatabaseMixin):
            _specific_database = 'default'

        self.not_select_class = NotSelectSpecificDatabase
        self.select_class = SelectSpecificDatabase

    def test_not_select_specific_database(self):
        not_select = self.not_select_class()

        with self.assertRaises(RequireSpecificDatabaseException):
            print(not_select.specific_database())

    def test_select_specific_database(self):
        select = self.select_class()
        self.assertEqual(select.specific_database(), 'default')
