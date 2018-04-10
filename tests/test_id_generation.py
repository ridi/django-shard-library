from django.test import TestCase
from django_dynamic_fixture import G

from tests.models import IdGenerateTestModel, TestIds


class TableStrategyTestCase(TestCase):
    def test_id_generation(self):
        dummy_one = G(IdGenerateTestModel)
        dummy_two = G(IdGenerateTestModel)
        self.assertEqual(dummy_one.id, 1)
        self.assertEqual(dummy_two.id, 2)

        id_generation_row_count = TestIds.objects.count()
        total_row_count = IdGenerateTestModel.objects.count()
        self.assertEqual(id_generation_row_count, total_row_count)
