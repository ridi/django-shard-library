from typing import Optional

from shard.strategy.routing.random import RandomReadStrategy


class BaseRouter:
    def db_for_read(self, model, **hints):
        raise NotImplementedError

    def db_for_write(self, model, **hints):
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

    def _get_master_database(self, model, **hints) -> Optional[str]:
        raise NotImplementedError

    def _get_slave_database(self, master: str) -> str:
        return self._strategy.pick_read_db(master=master)
