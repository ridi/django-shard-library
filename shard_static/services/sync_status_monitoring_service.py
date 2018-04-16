from typing import List, Dict

from shard.utils.database import get_master_databases_for_shard
from shard_static.models import StaticSyncStatus


def get_sync_status() -> Dict:
    databases = get_master_databases_for_shard()

    raw_datas = []
    for database in databases:
        raw_datas.append((database, StaticSyncStatus.objects.shard(shard=database).all()))

    return _assemble_status_data(raw_datas=raw_datas)


# [qs, qs, qs] -> {shard_model_key_one: {shard_1: last_modified}, shard_model_key_two: {}, }
def _assemble_status_data(raw_datas: List) -> Dict:
    result = {}

    for database, raw_data in raw_datas:
        for obj in raw_data:
            if obj.static_model_key not in result:
                result[obj.static_model_key] = {}
            result[obj.static_model_key][database] = obj.last_modified

    return result
