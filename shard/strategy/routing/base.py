from typing import List

from shard.utils.database import get_slave_databases_by_master


class BaseReadRoutingStrategy:
    @classmethod
    def get_slave_databases(cls, master: str) -> List:
        return get_slave_databases_by_master(master=master)

    @classmethod
    def pick_read_db(cls, master: str) -> str:
        raise NotImplementedError
