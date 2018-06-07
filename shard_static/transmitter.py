from typing import Optional, Type, Tuple, List, Any

from django.conf import settings
from django.db import transaction

from shard.constants import DEFAULT_DATABASE, DATABASE_CONFIG_SHARD_GROUP
from shard.utils.database import get_master_databases_by_shard_group
from shard_static.exceptions import InvalidDatabaseAliasException, NotShardStaticException, NotTransmitException
from shard_static.models import BaseShardStaticModel, BaseStaticTransmitStatus


class Transmitter:
    status_class: BaseStaticTransmitStatus = None

    def __init__(self, shard: str, model_class: Type[BaseShardStaticModel]):
        self.shard = shard
        self.model_class = model_class
        self.status = self._get_status()

        self._validate_model()
        self._validate_database()

    def run(self) -> List[BaseShardStaticModel]:
        next_criterion, items = self.collect()
        items = self.pre_transmit(items)

        with transaction.atomic(using=self.shard):
            items = self.transmit(items)
            items = self.post_transmit(items)
            self.save_status(next_criterion)

        return items

    def collect(self) -> Tuple[Any, List[BaseShardStaticModel]]:
        raise NotImplementedError

    def pre_transmit(self, source_items: List[BaseShardStaticModel]) -> List[BaseShardStaticModel]:
        raise NotImplementedError

    def transmit(self, items: List[BaseShardStaticModel]) -> List[BaseShardStaticModel]:
        raise NotImplementedError

    def post_transmit(self, items: List[BaseShardStaticModel]):
        raise NotImplementedError

    def save_status(self, next_criterion):
        self.status.criterion = next_criterion
        self.status.save(using=self.shard)

    def _get_status(self) -> BaseStaticTransmitStatus:
        status, _ = self.status_class.objects.get_or_create(shard=self.shard, key=self._make_transmit_key())
        return status

    def _validate_model(self):
        if not issubclass(self.model_class, BaseShardStaticModel):
            raise NotShardStaticException()

        if not self.model_class.transmit:
            raise NotTransmitException()

    def _validate_database(self):
        if self.shard == DEFAULT_DATABASE:
            raise InvalidDatabaseAliasException()

        if self._get_shard_group_from_database() is None:
            raise InvalidDatabaseAliasException()

        databases = get_master_databases_by_shard_group(shard_group=self.model_class.shard_group)
        if self.shard not in databases:
            raise InvalidDatabaseAliasException()

    def _get_shard_group_from_database(self) -> Optional[str]:
        db_setting = settings.DATABASES.get(self.shard, None)
        if db_setting:
            return db_setting.get(DATABASE_CONFIG_SHARD_GROUP, None)

        return None

    def _make_transmit_key(self) -> str:
        return self.model_class._meta.db_table  # flake8: noqa: W0212 pylint: disable=protected-access
