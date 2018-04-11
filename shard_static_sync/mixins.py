from shard_static_sync.constants import ALL_SHARD_GROUP


class ShardStaticMixin:
    shard_group = ALL_SHARD_GROUP

    # If difussible set true, exists source data in default
    # If difussible set false, only exists in shard database
    diffusible = True
