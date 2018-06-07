from django.test import TestCase
from django_dynamic_fixture import G

from shard.utils.database import get_master_databases_by_shard_group
from shard_static.exceptions import InvalidDatabaseAliasException, NotTransmitException
from tests.models import ShardStaticA, ShardStaticB, ShardStaticTransmittableB
from tests.transmitter import TestTransmitter


class TransmitterTestCase(TestCase):
    def setUp(self):
        self.items = [G(ShardStaticA), G(ShardStaticA), G(ShardStaticA), G(ShardStaticA)]

    def test_transmit_success(self):
        shard = get_master_databases_by_shard_group(ShardStaticA.shard_group)[0]

        transmitter = TestTransmitter(shard=shard, model_class=ShardStaticA)
        transmitter.run()

        self.assertEqual(len(ShardStaticA.objects.shard(shard=shard).all()), 4)
        self.assertEqual(transmitter.status.criterion, self.items[-1].id)

    def test_transmit_failure_when_mismatch_shard_group(self):
        shard = get_master_databases_by_shard_group(ShardStaticA.shard_group)[0]

        with self.assertRaises(InvalidDatabaseAliasException):
            transmitter = TestTransmitter(shard=shard, model_class=ShardStaticTransmittableB)
            transmitter.run()

    def test_transmit_failure_when_dont_transmittable(self):
        shard = get_master_databases_by_shard_group(ShardStaticB.shard_group)[0]

        with self.assertRaises(NotTransmitException):
            transmitter = TestTransmitter(shard=shard, model_class=ShardStaticB)
            transmitter.run()
