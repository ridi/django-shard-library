from django.apps import AppConfig

from shard.providers import pool_provider


class ShardAppConfig(AppConfig):
    name = 'shard'

    def ready(self):
        pool_provider.create()
