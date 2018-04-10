import uuid

from django.test import TestCase
from django_dynamic_fixture import G

from tests.models import IdGenerateTestModel, TestIds, UUIDTestModel


class TableStrategyTestCase(TestCase):
    def test_id_generation(self):
        dummy_one = G(IdGenerateTestModel)
        dummy_two = G(IdGenerateTestModel)
        self.assertEqual(dummy_one.id, 1)
        self.assertEqual(dummy_two.id, 2)

        id_generation_row_count = TestIds.objects.count()
        total_row_count = IdGenerateTestModel.objects.count()
        self.assertEqual(id_generation_row_count, total_row_count)


class UUIDStrategyTestCase(TestCase):
    def setUp(self):
        self.dummy_one = G(UUIDTestModel)
        self.dummy_two = G(UUIDTestModel)

    def test_uuid4_pk(self):
        uuid_one = uuid.UUID(hex=self.dummy_one.pk)
        uuid_two = uuid.UUID(hex=self.dummy_two.pk)

        self.assertEqual(uuid_one.hex, self.dummy_one.pk)
        self.assertEqual(uuid_two.hex, self.dummy_two.pk)
        self.assertNotEqual(self.dummy_one.pk, self.dummy_two.pk)
