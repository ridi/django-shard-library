from django.db import models

from shard.mixins import IsolatedShardMixin
from shard_static.managers import ShardStaticManager, ShardStaticStatusManager
from shard_static.mixins import ShardStaticMixin


class BaseStaticTransmitStatus(IsolatedShardMixin, models.Model):
    key = models.CharField(max_length=64, unique=True, verbose_name='Transmit Status Key')

    created = models.DateTimeField(auto_now_add=True, verbose_name='Created Datetime', )
    last_modified = models.DateTimeField(auto_now=True, verbose_name='Last Modified', )

    objects = ShardStaticStatusManager()

    class Meta:
        abstract = True

    @property
    def criterion(self):
        raise NotImplementedError

    @criterion.setter
    def criterion(self, criterion):
        raise NotImplementedError


class BaseShardStaticModel(ShardStaticMixin, models.Model):
    objects = ShardStaticManager()

    class Meta:
        abstract = True
