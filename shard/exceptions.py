from typing import List

__all__ = (
    'StrategyNotImplementException', 'RequireSpecificDatabaseException', 'RequireMasterConfigException', 'NotShardingModelException',
    'RequireShardKeyException', 'QueryExecuteFailureException',
)


class StrategyNotImplementException(Exception):
    pass


class RequireSpecificDatabaseException(Exception):
    pass


class RequireMasterConfigException(Exception):
    pass


class NotShardingModelException(Exception):
    pass


class RequireShardKeyException(Exception):
    pass


class QueryExecuteFailureException(Exception):
    def __init__(self, shard_group: str, executed: List, exception: Exception, *args, **kwargs):
        self.shard_group = shard_group
        self.executed = executed
        self.parent_exception = exception

        super().__init__(*args, **kwargs)
