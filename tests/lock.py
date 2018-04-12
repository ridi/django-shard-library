from shard_static.lock import BaseLockManager

_fake_cache = {}


class FakeLockManager(BaseLockManager):
    def is_locked(self) -> bool:
        return self.key in _fake_cache

    def lock(self) -> bool:
        if self.is_locked():
            return False

        _fake_cache[self.key] = self.uuid
        return True

    def release(self) -> bool:
        if self.is_locked():
            del _fake_cache[self.key]
            return True

        return False

    def ping(self) -> bool:
        return self.key in _fake_cache
