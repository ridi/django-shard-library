from typing import Dict, Optional

from shard.config.database_config import make_replication_configuration, make_shard_configuration

__all__ = ('ConfigHelper',)

DEFAULT_CONN_MAX_AGE = 0


class ConfigHelper:
    @staticmethod
    def generate_database_configs(unshard: Optional[Dict] = None, shard: Optional[Dict] = None) -> Dict:
        configuration = {}

        # Make Unshard Configuration
        if unshard:
            for key, config in unshard.items():
                configuration.update(make_replication_configuration(
                    key=key, master=config['master'], slaves=config.get('slaves', []),
                    conn_max_age=config.get('conn_max_age', DEFAULT_CONN_MAX_AGE)
                ))

        # Make Shard Configuration
        if shard:
            for shard_group, config in shard.items():
                configuration.update(make_shard_configuration(
                    shard_group=shard_group, database_name=config['database_name'], logical_count=config['logical_count'],
                    conn_max_age=config.get('conn_max_age', DEFAULT_CONN_MAX_AGE), shards=config['shards'],
                    options=config.get('options', {})
                ))

        return configuration
