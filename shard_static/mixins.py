from shard.constants import DEFAULT_DATABASE
from shard.mixins import BaseShardMixin


class ShardStaticMixin(BaseShardMixin):
    # If transmit set true, exists source database
    # If transmit set false, only exists in shard database
    transmit = True
    source_db = DEFAULT_DATABASE
