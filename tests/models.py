from django.db import models

from shard.fields import TableStrategyPkField
from shard.managers import ShardManager, ShardStaticManager
from shard.mixins import ShardStaticMixin, ShardMixin
from shard.models import TableStrategyModel


class ShardStaticAll(ShardStaticMixin, models.Model):
    objects = ShardStaticManager()


class ShardStaticA(ShardStaticMixin, models.Model):
    shard_group = 'shard_a'

    objects = ShardStaticManager()


class ShardStaticB(ShardStaticMixin, models.Model):
    shard_group = 'shard_b'
    diffusible = False

    objects = ShardStaticManager()


class ShardModelA(ShardMixin, models.Model):
    user_id = models.IntegerField(verbose_name='유저 idx')

    objects = ShardManager()

    shard_group = 'shard_a'
    shard_key_name = 'user_id'


class ShardModelB(ShardMixin, models.Model):
    user_id = models.IntegerField(verbose_name='유저 idx')

    objects = ShardManager()

    shard_group = 'shard_b'
    shard_key_name = 'user_id'


class NormalModel(models.Model):
    pass


class TestIds(TableStrategyModel):
    pass


class IdGenerateTestModel(models.Model):
    id = TableStrategyPkField(source_model='tests.TestIds', primary_key=True)
