import random

from shard.strategy.routing.base import BaseReadRoutingStrategy


class RandomReadStrategy(BaseReadRoutingStrategy):
    @classmethod
    def pick_read_db(cls, master: str):
        databases = cls.get_slave_databases(master=master)

        if not databases:
            return master

        return random.choice(databases)
