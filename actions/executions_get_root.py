from lib.action import St2BaseAction

__all__ = [
    'St2ExecutionGetRootAction'
]


class St2ExecutionGetRootAction(St2BaseAction):

    def get_parent(self, execution):
        if not hasattr(execution, 'parent'):
            return None

        parent_execution = self.client.executions.get_by_id(execution.parent)
        return parent_execution

    def get_root(self, execution):
        parent_execution = self.get_parent(execution)
        return self.get_root(parent_execution) if parent_execution else execution

    def run(self, id, exclude):
        execution = self.client.executions.get_by_id(id)
        root_execution = self.get_root(execution) if execution else None
        return root_execution.to_dict(exclude_attributes=exclude) if root_execution else None
