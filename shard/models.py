from django.db import models
from django.db.models import BigAutoField

from shard.mixins import SpecificDatabaseMixin


class TableStrategyModel(SpecificDatabaseMixin, models.Model):
    id = BigAutoField(primary_key=True)

    _specific_database = 'default'

    class Meta:
        abstract = True
