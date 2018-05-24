from typing import Dict

from shard.config.database_config import make_shard_configuration, make_replication_configuration

__all__ = ('ConfigHelper', )


class ConfigHelper:
    @staticmethod
    def generate_database_configs(unshard: Dict=None, shard: Dict=None) -> Dict:
        configuration = {}

        # Make Unshard Configuration
        if unshard:
            for key, config in unshard.items():
                configuration.update(make_replication_configuration(key=key, replication_config=config))

        # Make Shard Configuration
        if shard:
            for shard_group, config in shard.items():
                configuration.update(make_shard_configuration(
                    shard_group=shard_group, shard_options=config['shard_options'], shards=config['shards'],
                    db_options=config.get('db_options')
                ))

        return configuration
