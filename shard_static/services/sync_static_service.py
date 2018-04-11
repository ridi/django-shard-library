import logging
from typing import Optional, Type

from django.apps import apps
from django.conf import settings
from django.db import transaction

from shard.constants import DATABASE_CONFIG_SHARD_GROUP, DEFAULT_DATABASE
from shard.utils.database import get_master_databases_by_shard_group
from shard_static.constants import ALL_SHARD_GROUP
from shard_static.exceptions import InvalidDatabaseAliasException, NotDiffusibleException, NotShardStaticException
from shard_static.models import BaseShardStaticModel, StaticSyncStatus
from shard_static.services import lock_service

logger = logging.getLogger('shard_static.services.sync_static_service')


def sync_static(model_name: str, database_alias: str):
    model = _get_model(model_name=model_name)

    _validate_model(model)
    _validate_database(model, database_alias)

    lock_manager = lock_service.get_lock_manager(model_name, database_alias)
    if not lock_manager.lock():
        logger.info('Already exists processing - %s, %s' % (model_name, database_alias))

    try:
        sync_status, _ = StaticSyncStatus.objects.shard(shard=database_alias)\
            .get_or_create(key=model._meta.db_table)  # flake8: noqa: W0212 pylint: disable=protected-access

        origin_data = model.objects.find_by_last_modified(last_modified=sync_status.last_modified)
        # Limit Count check
        with transaction.atomic(database_alias):
            # update_or_create
            # update last_modified at sync_status
            pass

    finally:
        lock_manager.release()


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
    if model.shard_group != ALL_SHARD_GROUP and database_alias in databases:
        raise InvalidDatabaseAliasException()


def _get_shard_group_from_database(database_alias: str) -> Optional[str]:
    config = settings.DATABASES.get(database_alias, None)
    if config:
        return config.get(DATABASE_CONFIG_SHARD_GROUP, None)

    return None
