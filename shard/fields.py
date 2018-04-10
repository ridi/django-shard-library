from django.db import models

from shard.mixins import StrategyPkMixin


class TableStrategyPkField(StrategyPkMixin, models.BigAutoField):
    def __init__(self, source_model: str, *args, **kwargs):
        from shard.strategy.id_generation.table import TableStrategy
        self.source_model = source_model
        kwargs['strategy'] = TableStrategy(source_model=self.source_model)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['source_model'] = self.source_model

        return name, path, args, kwargs


class UUID4StrategyPkField(StrategyPkMixin, models.CharField):
    def __init__(self, *args, **kwargs):
        from shard.strategy.id_generation.uuid import UUIDStrategy
        kwargs['strategy'] = UUIDStrategy()

        # If null is false, field's default value is empty string.
        # So, model not call get_pk_value_on_save
        # If you will use this field, give up using migrations.
        # Crash django when using migrations, because django not supported nullable pk.
        kwargs['null'] = True
        super().__init__(*args, **kwargs)


class NanosecondStrategyPkField(StrategyPkMixin, models.BigAutoField):
    def __init__(self, *args, **kwargs):
        from shard.strategy.id_generation.nanosecond import NanosecondStrategy
        kwargs['strategy'] = NanosecondStrategy()
        super().__init__(*args, **kwargs)
