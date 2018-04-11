from django.db import models

from shard.managers import ShardStaticManager
from shard.mixins import ShardStaticMixin


class StaticSyncStatus(ShardStaticMixin, models.Model):
    static_model_key = models.CharField(max_length=64, verbose_name='Static Model Key')
    last_modified = models.DateTimeField(null=True, verbose_name='Last Modified', )

    diffusible = False

    objects = ShardStaticManager()

    class Meta:
        db_table = 'static_sync_status'
