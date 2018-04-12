from shard_static.constants import DEFAULT_LOCK_TTL
from shard_static.lock import BaseLockManager


class FakeLockManager(BaseLockManager):
    def __init__(self, key: str, ttl: int=DEFAULT_LOCK_TTL):
        super().__init__(key, ttl)
        self.is_locked = False

    def is_locked(self) -> bool:
        return self.is_locked

    def lock(self) -> bool:
        self.is_locked = True
        return self.is_locked

    def release(self) -> bool:
        self.is_locked = False
        return True

    def ping(self) -> bool:
        return True
