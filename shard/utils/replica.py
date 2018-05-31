from django.conf import settings

__all__ = ('get_replica_count', )

SHARD_REPLICA_COUNT_SETTING = 'SHARD_REPLICA_COUNT_SETTING'
DEFAULT_REPLICA_COUNT = 512


def get_replica_count(shard_group: str) -> int:
    replica_settings = _get_shard_replica_settings()
    return replica_settings.get(shard_group, DEFAULT_REPLICA_COUNT)


def _get_shard_replica_settings():
    return getattr(settings, SHARD_REPLICA_COUNT_SETTING, {})
