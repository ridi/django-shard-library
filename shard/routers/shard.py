from typing import Optional

from shard.constants import ALL_SHARD_GROUP
from shard.mixins import ShardMixin, ShardStaticMixin

from shard.routers.base import BaseReplicationRouter
from shard.utils.shard import get_shard_by_instance, get_shard_by_shard_key_and_shard_group


class ShardRouter(BaseReplicationRouter):
    def allow_relation(self, obj1, obj2, **hints):
        if issubclass(obj1, ShardMixin) and issubclass(obj2, ShardMixin):
            return self._get_master_database(model=obj1.__class__, hints={'instance': obj1}) ==\
                   self._get_master_database(model=obj2.__class__, hints={'instance': obj2})

        if (issubclass(obj1, ShardMixin) and issubclass(obj2, ShardStaticMixin)) or \
                (issubclass(obj1, ShardStaticMixin) and issubclass(obj2, ShardMixin)):
            return obj1.shard_group == obj2.shard_group or \
                   obj1.shard_group == ALL_SHARD_GROUP or \
                   obj2.shard_group == ALL_SHARD_GROUP

        if issubclass(obj1, ShardStaticMixin):
            return obj1.diffusible

        if issubclass(obj2, ShardStaticMixin):
            return obj2.diffusible

        return None

    def _get_master_database(self, model, **hints) -> Optional[str]:
        if not issubclass(model, ShardMixin):
            return None

        shard = None
        if hints.get('shard_key'):
            shard = get_shard_by_shard_key_and_shard_group(shard_key=hints['shard_key'], shard_group=model.shard_group)
        elif hints.get('instance'):
            shard = get_shard_by_instance(instance=hints['instance'])

        return shard
