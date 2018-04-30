from django.db import models

from shard_static.managers import ShardStaticManager
from shard_static.mixins import ShardStaticMixin


class BaseStaticSyncStatus(ShardStaticMixin, models.Model):
    static_model_key = models.CharField(max_length=64, unique=True, verbose_name='Static Model Key')

    diffusible = False

    objects = ShardStaticManager()

    class Meta:
        abstract = True
        db_table = 'static_sync_status'

    def set_revision(self, shard_static_model):
        raise NotImplementedError


class BaseShardStaticModel(ShardStaticMixin, models.Model):
    objects = ShardStaticManager()

    class Meta:
        abstract = True

    @classmethod
    def get_origin_data(cls, status):
        raise NotImplementedError
