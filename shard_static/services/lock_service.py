from shard_static.utils.lock.base import BaseLockManager


def get_lock_manager(model_name: str, database_alias: str) -> BaseLockManager:
    lock_key = _make_lock_key(model_name, database_alias)
    ttl = StaticSyncConfig.get_lock_ttl()
    lock_manager_class = get_class

    return lock_manager_class(key=lock_key, ttl=ttl)


def _make_lock_key(model_name: str, database_alias: str) -> str:
    return 'lock:%s:%s' % (model_name, database_alias)
