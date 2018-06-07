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

        self._validate_model()
        self._validate_database()

    def run(self):
        status = self._get_status()
        last_criterion, items = self.collect(status)
        items = self.pre_transmit(items)

        with transaction.atomic(using=self.shard):
            items = self.transmit(items)
            self.post_transmit(items)
            self._save_status(status, last_criterion)

    def collect(self, status: BaseStaticTransmitStatus) -> Tuple[Any, List[BaseShardStaticModel]]:
        raise NotImplementedError

    def pre_transmit(self, source_items: List[BaseShardStaticModel]) -> List[BaseShardStaticModel]:
        return source_items

    def transmit(self, items: List[BaseShardStaticModel]) -> List[BaseShardStaticModel]:
        raise NotImplementedError

    def post_transmit(self, items: List[BaseShardStaticModel]):
        return items

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

    def _get_status(self) -> BaseStaticTransmitStatus:
        status, _ = self.status_class.objects.get_or_create(shard=self.shard, key=self._make_transmit_key())
        return status

    def _save_status(self, status: BaseStaticTransmitStatus, last_criterion) -> BaseStaticTransmitStatus:
        status.criterion = last_criterion
        status.save(using=self.shard)

        return status

    def _make_transmit_key(self) -> str:
        return self.model_class._meta.db_table  # flake8: noqa: W0212 pylint: disable=protected-access
