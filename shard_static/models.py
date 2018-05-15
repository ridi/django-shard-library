from datetime import datetime, timezone

from django.db import models

from shard_static.managers import ShardStaticManager, ShardStaticStatusManager
from shard_static.mixins import ShardStaticMixin


def get_first_day() -> datetime:
    return datetime(1970, 1, 1, tzinfo=timezone.utc)


# Don't link StaticSyncStatus and other model.
# StaticSyncStatus is isolation each shards.
class StaticSyncStatus(models.Model):
    static_model_key = models.CharField(max_length=64, unique=True, verbose_name='Static Model Key')
    last_modified = models.DateTimeField(null=False, default=get_first_day, verbose_name='Last Modified', )

    objects = ShardStaticStatusManager()

    class Meta:
        db_table = 'static_sync_status'


class BaseShardStaticModel(ShardStaticMixin, models.Model):
    last_modified = models.DateTimeField(auto_now=True, db_index=True, verbose_name='Last Modified', )

    objects = ShardStaticManager()

    class Meta:
        abstract = True
