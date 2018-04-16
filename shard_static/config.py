from django.conf import settings

from shard_static.constants import DEFAULT_MAX_ITEMS, DEFAULT_LOCK_TTL

SHARD_SYNC_MAX_ITEMS = getattr(settings, 'SHARD_SYNC_MAX_ITEMS', DEFAULT_MAX_ITEMS)

SHARD_SYNC_LOCK_KEY_PREFIX = getattr(settings, 'SHARD_SYNC_LOCK_KEY_PREFIX', 'shard_sync_lock')
SHARD_SYNC_LOCK_TTL = getattr(settings, 'SHARD_SYNC_LOCK_TTL', DEFAULT_LOCK_TTL)
SHARD_SYNC_LOCK_MANAGER_CLASS = getattr(settings, 'SHARD_SYNC_LOCK_MANAGER_CLASS')
