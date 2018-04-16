from django.apps import apps

from shard.mixins import SpecificDatabaseMixin
from shard.routers.base import BaseRouter


class SpecificRouter(BaseRouter):
    def db_for_read(self, model, **hints):
        return self._get_specific_database(model=model, **hints)

    def db_for_write(self, model, **hints):
        return self._get_specific_database(model=model, **hints)

    def allow_relation(self, obj1, obj2, **hints):
        obj1_db = self._get_specific_database(model=obj1.__class__)
        obj2_db = self._get_specific_database(model=obj2.__class__)

        if obj1_db is None or obj2_db is None:
            return None

        return obj1_db == obj2_db

    def allow_migrate(self, db, app_label, model_name=None, **hints):
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

        specific_db = self._get_specific_database(model)
        if specific_db is None:
            return None

        return specific_db == db

    def _get_specific_database(self, model, **hints):
        if not issubclass(model, SpecificDatabaseMixin):
            return None

        return model.specific_database()
