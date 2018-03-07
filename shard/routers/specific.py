from shard.routers.base import BaseRouter
from shard.mixins import SpecificDatabaseMixin


class SpecificRouter(BaseRouter):
    def db_for_read(self, model, **hints):
        return self._get_specific_database(model=model, **hints)

    def db_for_write(self, model, **hints):
        return self._get_specific_database(model=model, **hints)

    def _get_specific_database(self, model, **hints):
        if not issubclass(model, SpecificDatabaseMixin):
            return None

        return model.specific_database()
