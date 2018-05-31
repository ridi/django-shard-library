from datetime import datetime

from django.db import models

from shard_static.managers import ShardStaticManager, ShardStaticStatusManager
from shard_static.mixins import ShardStaticMixin


def get_first_day() -> datetime:
    return datetime(1970, 1, 1)


# Don't link StaticTransmitStatus and other model.
# StaticTransmitStatus is isolation each shards.
class StaticTransmitStatus(models.Model):
    static_model_key = models.CharField(max_length=64, unique=True, verbose_name='Static Model Key')
    criterion_datetime = models.DateTimeField(null=False, default=get_first_day, verbose_name='Criterion Datetime', )

    created = models.DateTimeField(auto_now_add=True, verbose_name='Created Datetime', )
    last_modified = models.DateTimeField(auto_now=True, verbose_name='Last Modified', )

    objects = ShardStaticStatusManager()

    class Meta:
        db_table = 'static_transmit_status'


class BaseShardStaticModel(ShardStaticMixin, models.Model):
    last_modified = models.DateTimeField(auto_now=True, db_index=True, verbose_name='Last Modified', )

    objects = ShardStaticManager()

    class Meta:
        abstract = True
