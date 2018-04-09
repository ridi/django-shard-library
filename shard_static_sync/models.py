from django.db import models

from shard.mixins import ShardStaticMixin


class StaticSyncStatus(ShardStaticMixin, models.Model):
    static_model_key = models.CharField(max_length=64, verbose_name='Static Model Key')
    last_modified = models.DateTimeField(null=True, verbose_name='Last Modified', )

    is_locked = models.BooleanField(null=False, default=False, verbose_name='Is Locked')
    last_locked_time = models.DateTimeField(null=True, verbose_name='Last Locked Time')

    diffusible = False

    class Meta:
        db_table = 'shard_sync_status'
