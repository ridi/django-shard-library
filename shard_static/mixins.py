from shard.mixins import BaseShardMixin


class ShardStaticMixin(BaseShardMixin):
    # If transmit set true, exists source data in default
    # If transmit set false, only exists in shard database
    transmit = True
