from django.db import models

from shard.fields import TableStrategyPkField
from shard.managers import ShardManager
from shard.mixins import ShardMixin
from shard.models import TableStrategyModel
from shard_static.models import BaseShardStaticModel, BaseStaticSyncStatus


class StaticSyncStatus(BaseStaticSyncStatus):
    last_modified = models.DateTimeField(null=True)

    def set_revision(self, shard_static_model):
        if self.last_modified is None or self.last_modified < shard_static_model.last_modified:
            self.last_modified = shard_static_model.last_modified


class ShardStaticAll(BaseShardStaticModel, models.Model):
    last_modified = models.DateTimeField(null=False, auto_now=True,)
    @classmethod
    def get_origin_data(cls, status):
        if status.last_modified is None:
            return cls.objects.all()

        return cls.objects.filter(last_modified__gt=status.last_modified)


class ShardStaticA(BaseShardStaticModel, models.Model):
    last_modified = models.DateTimeField(null=False, auto_now=True,)
    shard_group = 'shard_a'

    @classmethod
    def get_origin_data(cls, status):
        if status.last_modified is None:
            return cls.objects.all()

        return cls.objects.filter(last_modified__gt=status.last_modified)


class ShardStaticB(BaseShardStaticModel, models.Model):
    last_modified = models.DateTimeField(null=False, auto_now=True,)

    shard_group = 'shard_b'
    diffusible = False

    @classmethod
    def get_origin_data(cls, status):
        if status.last_modified is None:
            return cls.objects.all()

        return cls.objects.filter(last_modified__gt=status.last_modified)


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
