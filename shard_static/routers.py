# pylint: disable=too-many-return-statements
from typing import Optional

from django.apps import apps
from django.conf import settings

from shard.constants import DATABASE_CONFIG_SHARD_GROUP, DEFAULT_DATABASE
from shard.mixins import ShardMixin
from shard.routers.base import BaseReplicationRouter
from shard.utils.shard import get_shard_by_shard_key_and_shard_group, get_shard_by_instance
from shard_static.exceptions import DontLinkException
from shard_static.mixins import ShardStaticMixin
from shard_static.models import StaticSyncStatus


class ShardStaticRouter(BaseReplicationRouter):
    def allow_relation(self, obj1, obj2, **hints):
        super_allow_relation = super().allow_relation(obj1, obj2, **hints)
        if super_allow_relation is not None:
            return super_allow_relation

        # Don't link StaticSyncStatus and other model.
        # StaticSyncStatus is isolation each shards.
        if isinstance(obj1, StaticSyncStatus) or isinstance(obj2, StaticSyncStatus):
            return False

        if isinstance(obj1, (ShardMixin, ShardStaticMixin)) and isinstance(obj2, (ShardMixin, ShardStaticMixin)):
            # obj1 and obj2 are for shard
            return obj1.shard_group == obj2.shard_group

        if (isinstance(obj1, (ShardMixin, ShardStaticMixin)) and not isinstance(obj2, (ShardMixin, ShardStaticMixin))) or \
                (not isinstance(obj1, (ShardMixin, ShardStaticMixin)) and isinstance(obj2, (ShardMixin, ShardStaticMixin))):

            # If you make relation shard obj and normal obj, raise exception.
            raise DontLinkException()

        # obj1 and obj2 are normal object.
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        super_allow_migrate = super().allow_migrate(db, app_label, model_name, **hints)
        if super_allow_migrate is not None:
            return super_allow_migrate

        model_name = model_name or hints.get('model_name')
        model = hints.get('model')
        if model:
            model_name = model.__name__

        if "." in model_name:
            _app_label = model_name.split('.')[0]
            app = apps.get_app_config(_app_label)
            model = app.get_model(model_name[len(_app_label) + 1:])
        else:
            app = apps.get_app_config(app_label)
            model = app.get_model(model_name)

        shard_group_for_db = settings.DATABASES[db].get(DATABASE_CONFIG_SHARD_GROUP, None)
        if not issubclass(model, (ShardMixin, ShardStaticMixin, StaticSyncStatus)):
            if shard_group_for_db:
                return False
            return None

        if issubclass(model, StaticSyncStatus):
            if db == DEFAULT_DATABASE or shard_group_for_db is None:
                return False
            return True

        if issubclass(model, ShardStaticMixin):
            if model.diffusible and db == DEFAULT_DATABASE:
                return True

        return shard_group_for_db == model.shard_group

    def _get_master_database(self, model, **hints) -> Optional[str]:
        if not issubclass(model, ShardMixin):
            return None

        shard = None
        if hints.get('shard_key'):
            shard = get_shard_by_shard_key_and_shard_group(shard_key=hints['shard_key'], shard_group=model.shard_group)
        elif hints.get('instance'):
            shard = get_shard_by_instance(instance=hints['instance'])

        return shard
