from django.db import models
from django.db.models import BigAutoField

from shard.constants import DEFAULT_DATABASE
from shard.mixins import SpecificDatabaseMixin


class TableStrategyModel(SpecificDatabaseMixin, models.Model):
    id = BigAutoField(primary_key=True)

    _specific_database = DEFAULT_DATABASE

    class Meta:
        abstract = True
