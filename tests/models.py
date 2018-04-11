from django.db import models

from shard.fields import TableStrategyPkField
from shard.managers import ShardManager
from shard.mixins import ShardMixin
from shard.models import TableStrategyModel
from shard_static.models import BaseShardStaticModel


class ShardStaticAll(BaseShardStaticModel, models.Model):
    pass


class ShardStaticA(BaseShardStaticModel, models.Model):
    shard_group = 'shard_a'


class ShardStaticB(BaseShardStaticModel, models.Model):
    shard_group = 'shard_b'
    diffusible = False


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
