from typing import List, Dict, Tuple

from django.test import TestCase

from shard.utils.consistent_hash.node import ConHashNode
from shard.utils.consistent_hash.pool import ConHashPool

_REPLICA_COUNT = 128


class ConHashPoolTest(TestCase):
    def test_make_ring(self):
        for pool_size in range(10, 16):
            pool = ConHashPool(list(range(pool_size)), _REPLICA_COUNT)
            self.assertEqual(len(pool._ring), pool._ring_length)
            self.assertEqual(max(pool._ring, key=lambda x: x.hash_value).hash_value, pool._ring[-1].hash_value)

    def test_decrease_node_count(self):
        data = list(range(100000))

        pool_one = ConHashPool(list(range(16)), _REPLICA_COUNT)
        pool_two = ConHashPool(list(range(15)), _REPLICA_COUNT)

        result_one = self._calc_result(pool_one, data)
        result_two = self._calc_result(pool_two, data)

        diff = self._diff_result(result_one, result_two)
        for one, _ in diff.values():
            self.assertEqual(one.index, 15)

    def _calc_result(self, pool: ConHashPool, data: List) -> Dict[int, ConHashNode]:
        result = {}

        for value in data:
            result[value] = pool.get_node(value=value)
        return result

    def _diff_result(self, result_one: Dict[int, ConHashNode], result_two: Dict[int, ConHashNode]) \
            -> Dict[int, Tuple[ConHashNode, ConHashNode]]:
        result = {}
        for key in range(100000):
            if result_one[key].index != result_two[key].index:
                result[key] = result_one[key], result_two[key]

        return result
