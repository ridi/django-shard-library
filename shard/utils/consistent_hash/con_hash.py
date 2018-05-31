import hashlib
from typing import Any


def md5_hash(value: Any) -> int:
    value = str(value)
    hash_value = int(hashlib.md5(value.encode('utf-8')).hexdigest(), 16) % (2 ** 64)
    return hash_value
