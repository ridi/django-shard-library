from django.db import models

from shard_static.constants import ALL_SHARD_GROUP
from shard_static.managers import ShardStaticManager, ShardStaticStatusManager
from shard_static.mixins import ShardStaticMixin


class StaticSyncStatus(models.Model):
    static_model_key = models.CharField(max_length=64, unique=True, verbose_name='Static Model Key')
    last_modified = models.DateTimeField(null=True, verbose_name='Last Modified', )

    shard_group = ALL_SHARD_GROUP
    objects = ShardStaticStatusManager()

    class Meta:
        db_table = 'static_sync_status'


class BaseShardStaticModel(ShardStaticMixin, models.Model):
    last_modified = models.DateTimeField(auto_now=True, db_index=True, verbose_name='Last Modified', )

    objects = ShardStaticManager()

    class Meta:
        abstract = True
