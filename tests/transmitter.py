from typing import List, Tuple

from shard_static.models import BaseShardStaticModel, BaseStaticTransmitStatus
from shard_static.transmitter import Transmitter
from tests.models import StaticTransmitStatus


class TestTransmitter(Transmitter):
    status_class = StaticTransmitStatus

    def collect(self, status: BaseStaticTransmitStatus) -> Tuple[int, List[BaseShardStaticModel]]:
        items = self.model_class.objects.filter(id__gte=status.criterion)

        if not items.exists():
            return status.criterion, []

        return items.last().id, items

    def transmit(self, items: List[BaseShardStaticModel]) -> List[BaseShardStaticModel]:
        self.model_class.objects.shard(shard=self.shard).bulk_create(objs=items)
        return items
