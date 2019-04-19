from django_dynamic_fixture import G

from shard.utils.database import get_master_databases_by_shard_group
from shard_static.exceptions import InvalidDatabaseAliasException, NotTransmitException
from tests.base import BaseTestCase
from tests.models import ShardStaticA, ShardStaticB, ShardStaticTransmittableB, StaticTransmitStatus
from tests.transmitter import TestTransmitter


class TransmitterTestCase(BaseTestCase):
    def setUp(self):
        self.items = [G(ShardStaticA), G(ShardStaticA), G(ShardStaticA), G(ShardStaticA)]

    def test_transmit_success(self):
        shard = get_master_databases_by_shard_group(ShardStaticA.shard_group)[0]

        transmitter = TestTransmitter(shard=shard, model_class=ShardStaticA)
        transmitter.run()

        status = StaticTransmitStatus.objects.shard(shard=shard).first()

        self.assertEqual(len(ShardStaticA.objects.shard(shard=shard).all()), 4)
        self.assertEqual(status.criterion, self.items[-1].id)

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
