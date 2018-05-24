import hashlib
from typing import Any


def con_hash(value: Any) -> int:
    value = str(value)
    hash_value = int(hashlib.sha256(value.encode('utf-8')).hexdigest(), 16) % (10 ** 8)
    return hash_value
