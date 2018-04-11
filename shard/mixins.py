from django.db import models

from shard.exceptions import StrategyNotImplementException, RequireSpecificDatabaseException

__all__ = ('StrategyPkMixin', 'SpecificDatabaseMixin', 'ShardMixin', )


class StrategyPkMixin(models.Field):
    def __init__(self, *args, **kwargs):
        strategy = kwargs.get('strategy', None)
        if strategy is None:
            raise StrategyNotImplementException

        self.strategy = strategy
        del kwargs['strategy']
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()

        kwargs['strategy'] = self.strategy
        return name, path, args, kwargs

    def get_pk_value_on_save(self, instance):
        if not instance.pk:
            return self.strategy.get_next_id(instance=instance)
        return instance.pk


class SpecificDatabaseMixin:
    _specific_database = None

    @classmethod
    def specific_database(cls):
        return cls._get_database()

    @classmethod
    def _get_database(cls):
        if cls._specific_database is None:
            raise RequireSpecificDatabaseException

        return cls._specific_database


class ShardMixin:
    shard_group = None
    shard_key_name = None

    def get_shard_key(self):
        return getattr(self, self.shard_key_name)
