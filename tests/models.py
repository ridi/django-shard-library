from django.db import models

from shard.fields import TableStrategyPkField
from shard.managers import ShardManager
from shard.mixins import ShardStaticMixin, ShardMixin
from shard.models import TableStrategyModel


class ShardStaticAll(ShardStaticMixin, models.Model):
    pass


class ShardStaticA(ShardStaticMixin, models.Model):
    shard_group = 'shard_a'
    diffusible = False


class ShardStaticB(ShardStaticMixin, models.Model):
    shard_group = 'shard_b'
    diffusible = False


class ShardModelA(ShardMixin, models.Model):
    user_id = models.IntegerField(verbose_name='유저 idx')
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    static_same = models.ForeignKey(ShardStaticA, null=True, on_delete=models.CASCADE)
    static_all = models.ForeignKey(ShardStaticAll, null=True, on_delete=models.CASCADE)

    objects = ShardManager()

    shard_group = 'shard_a'
    shard_key_name = 'user_id'


class ShardModelB(ShardMixin, models.Model):
    user_id = models.IntegerField(verbose_name='유저 idx')

    objects = ShardManager()

    shard_group = 'shard_b'
    shard_key_name = 'user_id'


class NormalModel(models.Model):
    normal_parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    static_all = models.ForeignKey(ShardStaticAll, null=True, on_delete=models.CASCADE)


class TestIds(TableStrategyModel):
    pass


class IdGenerateTestModel(models.Model):
    id = TableStrategyPkField(source_model='tests.TestIds', primary_key=True)
