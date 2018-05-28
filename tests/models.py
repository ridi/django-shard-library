from django.db import models

from shard.constants import DEFAULT_DATABASE
from shard.fields import TableStrategyPkField
from shard.managers import ShardManager
from shard.mixins import ShardMixin, SpecificDatabaseMixin
from shard.models import TableStrategyModel
from shard_static.models import BaseShardStaticModel


class ShardStaticA(BaseShardStaticModel, models.Model):
    text = models.CharField(null=True, max_length=32)

    shard_group = 'shard_a'


class ShardStaticB(BaseShardStaticModel, models.Model):
    shard_group = 'shard_b'
    transmit = False


class ShardModelA(ShardMixin, models.Model):
    user_id = models.IntegerField(verbose_name='유저 idx')
    text = models.CharField(max_length=64, null=False, blank=True, verbose_name='더미 텍스트')

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
