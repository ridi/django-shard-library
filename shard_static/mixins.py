
class ShardStaticMixin:
    shard_group = None

    # If transmit set true, exists source data in default
    # If transmit set false, only exists in shard database
    transmit = True
