from typing import List

from shard.utils.database import get_master_databases_for_shard
from shard_static.models import StaticSyncStatus


def get_sync_status() -> List:
    databases = get_master_databases_for_shard()

    raw_datas = []
    for database in databases:
        raw_datas.append(StaticSyncStatus.objects.shard(shard=database).all())

    return _assemble_status_data(raw_datas=raw_datas)


def _assemble_status_data(raw_datas: List) -> List:
    pass
