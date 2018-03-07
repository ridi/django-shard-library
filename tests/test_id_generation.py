import uuid
from unittest.mock import MagicMock, patch

from django.test import TestCase
from django_dynamic_fixture import G
from django_fake_model import models as f

from shard.models import TableStrategyModel
from shard.fields import UUID4StrategyPkField, TableStrategyPkField


class TestIds(f.FakeModel, TableStrategyModel):
    pass


class IdGenerateTestModel(f.FakeModel):
    id = TableStrategyPkField(source_model='TestIds', primary_key=True)


class UUIDTestModel(f.FakeModel):
    id = UUID4StrategyPkField(primary_key=True, max_length=32, verbose_name='UUID Pk field')


@patch('shard.strategy.id_generation.table.TableStrategy._get_model', MagicMock(return_value=TestIds))
@TestIds.fake_me
@IdGenerateTestModel.fake_me
class TableStrategyTestCase(TestCase):
    def test_id_generation(self):
        dummy_one = G(IdGenerateTestModel)
        dummy_two = G(IdGenerateTestModel)
        self.assertEqual(dummy_one.id, 1)
        self.assertEqual(dummy_two.id, 2)

        id_generation_row_count = TestIds.objects.count()
        total_row_count = IdGenerateTestModel.objects.count()
        self.assertEqual(id_generation_row_count, total_row_count)


@UUIDTestModel.fake_me
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
