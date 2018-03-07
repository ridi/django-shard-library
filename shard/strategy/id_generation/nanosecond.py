import random
import time

from django.utils.deconstruct import deconstructible
from shard.utils.shard_key import get_shard_key_from_instance

from shard.strategy.id_generation.base import BaseIDGenerationStrategy

__all__ = ('NanosecondStrategy', )


_NANO_SECOND = 1000000
_SHARD_KEY_BIT_LEN = (1 << 10)

_NANO_SECOND_PLACE_VALUE = 13
_SHARD_KEY_BIT_PLACE_VALUE = 3


@deconstructible
class NanosecondStrategy(BaseIDGenerationStrategy):
    def get_next_id(self, instance):
        # nanosecond 51 bit
        # shard_key_bit 10 bit
        # randint 3 bit
        # total 64 bit

        nanosecond = int(time.time() * _NANO_SECOND)
        shard_key_bit = get_shard_key_from_instance(instance) % _SHARD_KEY_BIT_LEN

        _rand = random.Random(id(object()))
        _randint = _rand.randint(0, 7)

        return nanosecond << _NANO_SECOND_PLACE_VALUE | shard_key_bit << _SHARD_KEY_BIT_PLACE_VALUE | _randint
