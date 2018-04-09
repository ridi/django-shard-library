
DEFAULT_LOCK_TTL = 60 * 5


class LockHelper:
    def __init__(self, key: str, ttl: int=DEFAULT_LOCK_TTL, *args, **kwargs):
        self.key = key
        self.ttl = ttl

    def is_locked(self):
        raise NotImplementedError()

    def lock(self):
        raise NotImplementedError()

    def ping(self):
        raise NotImplementedError()

    def release(self):
        raise NotImplementedError()
