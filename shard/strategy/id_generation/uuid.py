import uuid

from django.utils.deconstruct import deconstructible

from shard.strategy.id_generation.base import BaseIDGenerationStrategy

__all__ = ('UUIDStrategy', )


@deconstructible
class UUIDStrategy(BaseIDGenerationStrategy):
    def get_next_id(self, instance):
        return uuid.uuid4().hex
