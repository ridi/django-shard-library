import logging
from datetime import datetime
from typing import Optional, Type, List

from django.apps import apps
from django.conf import settings
from django.db import transaction
from django.forms import model_to_dict

from shard.constants import DATABASE_CONFIG_SHARD_GROUP, DEFAULT_DATABASE
from shard.utils.database import get_master_databases_by_shard_group
from shard_static import config
from shard_static.exceptions import InvalidDatabaseAliasException, NotDiffusibleException, NotShardStaticException
from shard_static.models import BaseShardStaticModel, StaticSyncStatus
from shard_static.services import lock_service

logger = logging.getLogger('shard_static.services.sync_static_service')


def run_sync_with_lock(model_name: str, database_alias: str):
    lock_manager = lock_service.get_lock_manager(model_name, database_alias)
    if not lock_manager.lock():
        logger.info(f'Already exists processing - {model_name}, {database_alias}')
        return

    try:
        run_sync(model_name=model_name, database_alias=database_alias)
    finally:
        lock_manager.release()


def run_sync(model_name: str, database_alias: str):
    model = _get_model(model_name=model_name)

    _validate_model(model)
    _validate_database(model, database_alias)

    sync_status, _ = StaticSyncStatus.objects.shard(shard=database_alias).get_or_create(static_model_key=_make_sync_key(model=model))

    offset = 0
    limit = config.SHARD_SYNC_MAX_ITEMS
    while True:
        source_items = model.objects.find_by_last_modified(last_modified=sync_status.last_modified, offset=offset, limit=limit)
        logger.debug(
            f'[Load source items] - last_modified: {sync_status.last_modified}, offset: {offset}, limit: {limit}',
            extra={'offset': offset, 'limit': limit, 'last_modified': sync_status.last_modified}
        )

        if source_items.count() == 0:
            logger.debug('Source Items Count: 0')
            return

        last_modified = _insert_items(items=source_items, model=model, database_alias=database_alias)

        if sync_status.last_modified != last_modified:
            sync_status.last_modified = last_modified
            sync_status.save(using=database_alias)
            return

        offset += limit


def _insert_items(items: List, model: Type[BaseShardStaticModel], database_alias) -> datetime:
    last_modified = None
    with transaction.atomic(database_alias):
        for _data in items:
            if not last_modified or last_modified < _data.last_modified:
                last_modified = _data.last_modified

            model.objects.shard(shard=database_alias).update_or_create(
                id=_data.id,
                defaults=model_to_dict(
                    _data, fields=[field.name for field in _data._meta.fields]  # flake8: noqa: W0212 pylint: disable=protected-access
                )
            )

    return last_modified


def _get_model(model_name: str) -> Type[BaseShardStaticModel]:
    _splited = model_name.split('.')
    _label, _model_name = _splited[0], _splited[1]

    app = apps.get_app_config(_label)
    model = app.get_model(_model_name)
    return model


def _validate_model(model: Type[BaseShardStaticModel]):
    if not issubclass(model, BaseShardStaticModel):
        raise NotShardStaticException()

    if not model.diffusible:
        raise NotDiffusibleException()


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


def _make_sync_key(model: Type[BaseShardStaticModel]):
    return model._meta.db_table  # flake8: noqa: W0212 pylint: disable=protected-access
