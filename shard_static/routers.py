# pylint: disable=too-many-return-statements
from typing import Optional

from django.apps import apps
from django.conf import settings

from shard.constants import DATABASE_CONFIG_SHARD_GROUP
from shard.mixins import IsolatedShardMixin, ShardMixin
from shard.routers.base import BaseReplicationRouter
from shard.utils.shard import get_shard_by_instance, get_shard_by_shard_key_and_shard_group
from shard_static.exceptions import DontLinkException
from shard_static.mixins import ShardStaticMixin


class ShardStaticRouter(BaseReplicationRouter):
    def allow_relation(self, obj1, obj2, **hints):
        # Don't link IsolatedShardMixin and other model.
        # IsolatedShardMixin is isolation each shards.
        if isinstance(obj1, IsolatedShardMixin) or isinstance(obj2, IsolatedShardMixin):
            return False

        if isinstance(obj1, (ShardMixin, ShardStaticMixin)) and isinstance(obj2, (ShardMixin, ShardStaticMixin)):
            # if obj1 and obj2 are shard static model, all config of them have to be same.
            if isinstance(obj1, ShardStaticMixin) and isinstance(obj2, ShardStaticMixin):
                return obj1.shard_group == obj2.shard_group and obj1.source_db == obj2.source_db and obj1.transmit == obj2.transmit
            elif isinstance(obj1, ShardMixin) and isinstance(obj2, ShardMixin):
                return super().allow_relation(obj1, obj2, **hints)
            else:
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

        if model_name is None:
            return None

        if "." in model_name:
            _app_label = model_name.split('.')[0]
            app = apps.get_app_config(_app_label)
            model = app.get_model(model_name[len(_app_label) + 1:])
        else:
            app = apps.get_app_config(app_label)
            model = app.get_model(model_name)

        shard_group_for_db = settings.DATABASES[db].get(DATABASE_CONFIG_SHARD_GROUP, None)
        if not issubclass(model, (ShardMixin, ShardStaticMixin, IsolatedShardMixin)):
            if shard_group_for_db:
                return False
            return None

        if issubclass(model, ShardStaticMixin):
            if model.transmit and db == model.source_db:
                return True

        return shard_group_for_db == model.shard_group

    def _get_master_database(self, model, **hints) -> Optional[str]:
        if not issubclass(model, (ShardMixin, ShardStaticMixin)):
            return None

        if issubclass(model, ShardStaticMixin):
            if model.transmit:
                return model.source_db
            else:
                return None

        shard = None
        if hints.get('shard_key'):
            shard = get_shard_by_shard_key_and_shard_group(shard_key=hints['shard_key'], shard_group=model.shard_group)
        elif hints.get('instance'):
            shard = get_shard_by_instance(instance=hints['instance'])

        return shard
