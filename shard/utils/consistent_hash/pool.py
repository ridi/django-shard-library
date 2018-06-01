from typing import Any, List

from shard.utils.consistent_hash import con_hash
from shard.utils.consistent_hash.node import ConHashNode

_MAX_32BIT_INTEGER = 2147483647


class ConHashPool:
    def __init__(self, nodes: List[str], replica: int):
        self._nodes = nodes
        self._replica = replica
        self._ring_length = len(nodes) * replica
        self._ring = []

        self.make_ring()

    def get_node(self, value: Any) -> 'ConHashNode':
        hash_value = self._hash(value=value)
        node_pos = self.get_node_pos(hash_value=hash_value)

        return self._ring[node_pos]

    def get_node_pos(self, hash_value: int) -> int:
        return self._get_node_pos(hash_value=hash_value, min_pos=0, max_pos=self._ring_length - 1)

    def make_ring(self):
        for index, node in enumerate(self._nodes):
            self._make_ring_for_node(node=node, node_index=index, replica=self._replica)

        self._ring.sort(key=lambda x: x.hash_value)

    def _get_node_pos(self, hash_value: int, min_pos: int, max_pos: int):
        if self._ring[min_pos].hash_value >= hash_value or \
                self._ring[max_pos].hash_value < hash_value or \
                min_pos == max_pos:
            return min_pos

        mid_pos = int((min_pos + max_pos) / 2)
        if self._ring[mid_pos].hash_value < hash_value:
            return self._get_node_pos(hash_value=hash_value, min_pos=mid_pos + 1, max_pos=max_pos)

        return self._get_node_pos(hash_value=hash_value, min_pos=min_pos, max_pos=mid_pos)

    def _make_ring_for_node(self, node: str, node_index: int, replica: int):
        _hash_index = 0
        _start_index = 0

        while _start_index < replica:
            pseudo_name = self._make_pseudo_name(node=node, node_index=node_index, hash_index=_hash_index)
            hash_value = self._hash(pseudo_name)
            _hash_index += 1

            if self._has_hash(hash_value=hash_value):
                continue

            self._ring.append(ConHashNode(hash_value=hash_value, index=node_index))
            _start_index += 1

    def _make_pseudo_name(self, node: str, node_index: int, hash_index: int) -> str:
        _dummy = hash_index * _MAX_32BIT_INTEGER
        return f"{node}:{node_index}:{hash_index}:{_dummy}"

    def _has_hash(self, hash_value: int) -> bool:
        for item in self._ring:
            if item.hash_value == hash_value:
                return True

        return False

    def _hash(self, value: Any) -> int:
        return con_hash.blake2b_hash(value)
