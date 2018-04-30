from django.db import models

from shard_static.constants import ALL_SHARD_GROUP
from shard_static.managers import ShardStaticManager, ShardStaticStatusManager
from shard_static.mixins import ShardStaticMixin


class BaseStaticSyncStatus(models.Model):
    static_model_key = models.CharField(max_length=64, unique=True, verbose_name='Static Model Key')

    shard_group = ALL_SHARD_GROUP
    objects = ShardStaticStatusManager()

    class Meta:
        abstract = True

    def record_status(self, shard_static_model):
        raise NotImplementedError


class BaseShardStaticModel(ShardStaticMixin, models.Model):
    objects = ShardStaticManager()

    class Meta:
        abstract = True

    @classmethod
    def get_origin_data(cls, status):
        raise NotImplementedError
