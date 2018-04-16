from django.test import TestCase

from shard.utils.execute import QueryExecutor


class ExecuteTestCase(TestCase):
    def setUp(self):
        self.shard_group = 'shard_a'

    def test_executor(self):
        executer = QueryExecutor(shard_group=self.shard_group)
        executed = executer.run_query(query='SELECT 1')

        self.assertEqual(executed, executer.get_shards())
