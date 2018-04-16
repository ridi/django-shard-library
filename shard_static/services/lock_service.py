from importlib import import_module
from typing import Type

from shard_static import config
from shard_static.lock import BaseLockManager


def get_lock_manager(model_name: str, database_alias: str) -> BaseLockManager:
    lock_key = _make_lock_key(model_name, database_alias)
    ttl = config.SHARD_SYNC_LOCK_TTL
    lock_manager_class = _import_lock_manager_class()

    return lock_manager_class(key=lock_key, ttl=ttl)


def _make_lock_key(model_name: str, database_alias: str) -> str:
    return f'{config.SHARD_SYNC_LOCK_KEY_PREFIX}:{model_name}:{database_alias}'


def _import_lock_manager_class() -> Type[BaseLockManager]:
    mod_path, _, cls_name = config.SHARD_SYNC_LOCK_MANAGER_CLASS.rpartition('.')
    mod = import_module(mod_path)
    cls = getattr(mod, cls_name)
    return cls
