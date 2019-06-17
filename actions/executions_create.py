from lib.action import St2BaseAction
from st2client.models.action import Execution
from st2client.commands.resource import ResourceNotFoundError

__all__ = [
    'St2ExecutionsCreateAction'
]


def format_result(item):
    if not item:
        return None

    return item.to_dict()


class St2ExecutionsCreateAction(St2BaseAction):
    def run(self, action, parameters=None, user=None, delay=None, trace_id=None, trace_tag=None):
        parameters = parameters or {}

        action_resource = self.client.managers['Action'].get_by_ref_or_id(action)
        if not action_resource:
            raise ResourceNotFoundError('Action "%s" cannot be found.'
                                        % action)
        action_ref = '.'.join([action_resource.pack, action_resource.name])

        execution = Execution()
        execution.action = action_ref
        execution.parameters = parameters

        if user:
            execution.user = user

        if delay:
            execution.delay = delay

        if not trace_id and trace_tag:
            execution.context = {'trace_context': {'trace_tag': trace_tag}}

        if trace_id:
            execution.context = {'trace_context': {'id_': trace_id}}

        result = self.client.executions.create(instance=execution)
        result = format_result(item=result)
        return result
