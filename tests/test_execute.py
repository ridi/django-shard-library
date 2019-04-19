from shard.utils.execute import QueryExecutor
from tests.base import BaseTestCase


class ExecuteTestCase(BaseTestCase):
    def setUp(self):
        self.shard_group = 'shard_a'

    def test_executor(self):
        executer = QueryExecutor(shard_group=self.shard_group)
        executed = executer.run_query(query='SELECT 1')

        self.assertEqual(executed, executer.get_shards())
