from typing import Optional

from django.conf import settings

from shard.strategy.routing.random import RandomReadStrategy


class BaseRouter:
    def db_for_read(self, model, **hints):
        raise NotImplementedError

    def db_for_write(self, model, **hints):
        raise NotImplementedError

    def allow_relation(self, obj1, obj2, **hints):
        raise NotImplementedError

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        raise NotImplementedError


class BaseReplicationRouter(BaseRouter):
    _strategy = RandomReadStrategy

    def db_for_read(self, model, **hints):
        master = self._get_master_database(model=model, **hints)

        if master is None:
            return None

        return self._get_slave_database(master=master)

    def db_for_write(self, model, **hints):
        return self._get_master_database(model=model, **hints)

    def allow_relation(self, obj1, obj2, **hints):
        obj1_db = self._get_master_database(model=obj1.__class__, instance=obj1)
        obj2_db = self._get_master_database(model=obj2.__class__, instance=obj2)

        # If variable is none, has not opinion for allow_relation.
        if obj1_db is None or obj2_db is None:
            return None

        return obj1_db == obj2_db

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # If db is slave, return false
        if settings.DATABASES[db].get('PRIMARY', None):
            return False

        return None

    def _get_master_database(self, model, **hints) -> Optional[str]:
        raise NotImplementedError

    def _get_slave_database(self, master: str) -> str:
        return self._strategy.pick_read_db(master=master)
