from django.db import models

from shard_static.managers import ShardStaticManager
from shard_static.mixins import ShardStaticMixin


class StaticSyncStatus(ShardStaticMixin, models.Model):
    static_model_key = models.CharField(max_length=64, unique=True, verbose_name='Static Model Key')
    last_modified = models.DateTimeField(null=True, verbose_name='Last Modified', )

    diffusible = False

    objects = ShardStaticManager()

    class Meta:
        db_table = 'static_sync_status'


class BaseShardStaticModel(ShardStaticMixin, models.Model):
    last_modified = models.DateTimeField(null=False, verbose_name='Last Modified', )

    objects = ShardStaticManager()

    class Meta:
        abstract = True
