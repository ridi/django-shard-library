from hashlib import blake2b
from typing import Any


def blake2b_hash(value: Any) -> int:
    value = str(value)
    hash_value = int(blake2b(value.encode('utf-8')).hexdigest(), 16) % (2 ** 64)
    return hash_value
