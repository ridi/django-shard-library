import logging
from typing import Optional, Type

from django.apps import apps
from django.conf import settings
from django.db import transaction
from django.forms import model_to_dict

from shard.constants import DATABASE_CONFIG_SHARD_GROUP, DEFAULT_DATABASE
from shard.utils.database import get_master_databases_by_shard_group
from shard_static import config
from shard_static.exceptions import InvalidDatabaseAliasException, NotDiffusibleException, NotShardStaticException, \
    TooManySyncItemsException
from shard_static.models import BaseShardStaticModel, StaticSyncStatus
from shard_static.services import lock_service

logger = logging.getLogger('shard_static.services.sync_static_service')


def sync_static(model_name: str, database_alias: str):
    model = _get_model(model_name=model_name)

    _validate_model(model)
    _validate_database(model, database_alias)

    lock_manager = lock_service.get_lock_manager(model_name, database_alias)
    if not lock_manager.lock():
        logger.info(f'Already exists processing - {model_name}, {database_alias}')

    try:
        _sync(model=model, database_alias=database_alias)
    except TooManySyncItemsException:
        logger.warning(f'[WARNING] {model_name}:{database_alias} greater than or equal to MAX_ITEMS')
    except:  # flake8: noqa: E722 pylint: disable=bare-except
        logger.exception(f'[EXCEPTION] {model_name}:{database_alias} raise exceptions while syncing')
    finally:
        lock_manager.release()


def _sync(model: Type[BaseShardStaticModel], database_alias: str):
    sync_status, _ = StaticSyncStatus.objects.shard(shard=database_alias) \
        .get_or_create(static_model_key=_make_sync_key(model=model))
    origin_data = model.objects.find_by_last_modified(last_modified=sync_status.last_modified)

    if origin_data.count() >= config.SHARD_SYNC_MAX_ITEMS:
        raise TooManySyncItemsException()

    with transaction.atomic(database_alias):
        last_modified = None
        for _data in origin_data:
            if not last_modified or last_modified < _data.last_modified:
                last_modified = _data.last_modified

            model.objects.shard(shard=database_alias).update_or_create(
                id=_data.id,
                defaults=model_to_dict(
                    _data, fields=[field.name for field in _data._meta.fields]  # flake8: noqa: W0212 pylint: disable=protected-access
                )
            )

        sync_status.last_modified = last_modified
        sync_status.save()


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
