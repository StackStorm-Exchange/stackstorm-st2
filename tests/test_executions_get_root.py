from base import BaseActionTestCase
from executions_get_root import St2ExecutionGetRootAction


class St2ExecutionGetRootActionTest(BaseActionTestCase):
    __test__ = True
    action_cls = St2ExecutionGetRootAction

    def _mock_get_by_id(self, id):
        if id in EXECUTION_RESULTS:
            return EXECUTION_RESULTS[id]

    def test_get_parent_execution(self):
        action = self.get_action_instance(self.full_config)

        # register mock processing of sending request to get execution result
        action.client.executions.get_by_id = self._mock_get_by_id

        # run with parent execution id
        result = action.run('a', [])
        self.assertEqual(result, {'id': 'a'})

        # run with child execution id
        for id in ['b', 'c']:
            result = action.run(id, [])
            self.assertEqual(result, {'id': 'a'})

        # run with invalid execution id
        result = action.run('invalid-id', [])
        self.assertIsNone(result)


class ResultMock(object):
    def __init__(self, current_id, parent_id=None):
        self.id = current_id
        if parent_id:
            self.parent = parent_id

    def to_dict(self, *args, **kwargs):
        return {'id': self.id}


# register mock execution results
EXECUTION_RESULTS = {
    'a': ResultMock(current_id='a'),
    'b': ResultMock(current_id='b', parent_id='a'),
    'c': ResultMock(current_id='c', parent_id='b'),
}
