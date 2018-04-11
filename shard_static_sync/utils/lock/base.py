
DEFAULT_LOCK_TTL = 60 * 5


class LockHelper:
    def __init__(self, key: str, ttl: int=DEFAULT_LOCK_TTL):
        self.key = key
        self.ttl = ttl

    def is_locked(self) -> bool:
        raise NotImplementedError()

    def lock(self) -> bool:
        raise NotImplementedError()

    def ping(self) -> bool:
        raise NotImplementedError()

    def release(self) -> bool:
        raise NotImplementedError()
