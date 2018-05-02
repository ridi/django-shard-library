from django.db import models

from shard_static.managers import ShardStaticManager, ShardStaticStatusManager
from shard_static.mixins import ShardStaticMixin


# Don't link StaticSyncStatus and other model.
# StaticSyncStatus is isolation each shards.
class StaticSyncStatus(models.Model):
    static_model_key = models.CharField(max_length=64, unique=True, verbose_name='Static Model Key')
    last_modified = models.DateTimeField(null=True, verbose_name='Last Modified', )

    objects = ShardStaticStatusManager()

    class Meta:
        db_table = 'static_sync_status'


class BaseShardStaticModel(ShardStaticMixin, models.Model):
    last_modified = models.DateTimeField(auto_now=True, db_index=True, verbose_name='Last Modified', )

    objects = ShardStaticManager()

    class Meta:
        abstract = True
