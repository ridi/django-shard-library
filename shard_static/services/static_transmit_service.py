import logging
from datetime import datetime
from typing import Optional, Type, List, Dict

from django.apps import apps
from django.conf import settings
from django.forms import model_to_dict

from shard.constants import DATABASE_CONFIG_SHARD_GROUP, DEFAULT_DATABASE
from shard.utils.database import get_master_databases_by_shard_group
from shard_static import config
from shard_static.exceptions import InvalidDatabaseAliasException, NotTransmitException, NotShardStaticException
from shard_static.models import BaseShardStaticModel, StaticTransmitStatus
from shard_static.services import lock_service

__all__ = ('run_transmit_with_lock', 'run_transmit', )

logger = logging.getLogger('shard_static.services.static_transmit_service')


_BATCH_SIZE = 1000


def run_transmit_with_lock(model_name: str, database_alias: str):
    lock_manager = lock_service.get_lock_manager(model_name, database_alias)
    if not lock_manager.lock():
        logger.info(f'Already exists processing - {model_name}, {database_alias}')
        return

    try:
        run_transmit(model_name=model_name, database_alias=database_alias)
    finally:
        lock_manager.release()


def run_transmit(model_name: str, database_alias: str):
    model = _get_model(model_name=model_name)

    _validate_model(model)
    _validate_database(model, database_alias)

    transmit_status, _ = StaticTransmitStatus.objects.shard(shard=database_alias)\
        .get_or_create(static_model_key=_make_transmit_key(model=model))

    offset = 0
    limit = config.SHARD_TRANSMIT_MAX_ITEMS
    while True:
        source_items = model.objects.find_by_last_modified(last_modified=transmit_status.criterion_datetime, offset=offset, limit=limit)
        logger.debug(
            f'[Load source items] - criterion_datetime: {transmit_status.criterion_datetime}, offset: {offset}, limit: {limit}',
            extra={'offset': offset, 'limit': limit, 'criterion_datetime': transmit_status.criterion_datetime}
        )

        if source_items.count() == 0:
            logger.debug('Source Items Count: 0')
            return

        last_modified = _insert_items(items=source_items, model=model, database_alias=database_alias)

        if transmit_status.criterion_datetime != last_modified:
            transmit_status.criterion_datetime = last_modified
            transmit_status.save(using=database_alias)
            return

        offset += limit


def _insert_items(items: List, model: Type[BaseShardStaticModel], database_alias: str) -> datetime:
    last_modified = None
    exist_item_ids = model.objects.shard(shard=database_alias).filter(id__in=[item.id for item in items]).values_list('id', flat=True)

    entities = []
    for item in items:
        if not last_modified or last_modified < item.last_modified:
            last_modified = item.last_modified

        if item.id in exist_item_ids:
            data = _get_data(item)

            logger.debug(f'[Insert items] Update {item.id}')
            model.objects.shard(shard=database_alias).filter(id=item.id).update(**data)
        else:
            entities.append(item)

    if entities:
        logger.debug(f'[Insert items] Bulk Create {len(entities)}')
        model.objects.shard(shard=database_alias).bulk_create(entities, _BATCH_SIZE)

    return last_modified


def _get_data(instance: BaseShardStaticModel) -> Dict:
    data = {}

    for field in instance._meta.fields:  # flake8: noqa: W0212 pylint: disable=protected-access
        data[field.name] = field.value_from_object(instance)

    return data


def _get_model(model_name: str) -> Type[BaseShardStaticModel]:
    _splited = model_name.split('.')
    _label, _model_name = _splited[0], _splited[1]

    app = apps.get_app_config(_label)
    model = app.get_model(_model_name)
    return model


def _validate_model(model: Type[BaseShardStaticModel]):
    if not issubclass(model, BaseShardStaticModel):
        raise NotShardStaticException()

    if not model.transmit:
        raise NotTransmitException()


def _validate_database(model: Type[BaseShardStaticModel], database_alias: str):
    if database_alias == DEFAULT_DATABASE:
        raise InvalidDatabaseAliasException()

    if _get_shard_group_from_database(database_alias) is None:
        raise InvalidDatabaseAliasException()

    databases = get_master_databases_by_shard_group(shard_group=model.shard_group)
    if database_alias not in databases:
        raise InvalidDatabaseAliasException()


def _get_shard_group_from_database(database_alias: str) -> Optional[str]:
    db_setting = settings.DATABASES.get(database_alias, None)
    if db_setting:
        return db_setting.get(DATABASE_CONFIG_SHARD_GROUP, None)

    return None


def _make_transmit_key(model: Type[BaseShardStaticModel]):
    return model._meta.db_table  # flake8: noqa: W0212 pylint: disable=protected-access
