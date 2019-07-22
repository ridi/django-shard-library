from functools import wraps
from typing import Callable


def memorize(func: Callable):
    _cache = {}

    @wraps(func)
    def _decorator(*args, clear: bool = False, nocache: bool = False, **kwargs):
        key = func.__name__ + str(args) + str(kwargs)
        if clear or nocache or key not in _cache:
            result = func(*args, **kwargs)
            if nocache:
                return result
            else:
                _cache[key] = result

        return _cache[key]

    return _decorator
