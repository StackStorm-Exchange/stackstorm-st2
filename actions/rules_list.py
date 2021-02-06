from lib.action import St2BaseAction
from lib.formatters import format_client_list_result

__all__ = [
    'St2RulesListAction'
]


def format_result(result, exclude_attributes):
    return format_client_list_result(result=result, exclude_attributes=exclude_attributes)


class St2RulesListAction(St2BaseAction):
    def run(self, pack=None, limit=None, exclude=None):
        kwargs = {}

        if limit:
            kwargs['limit'] = limit

        if pack:
            kwargs['pack'] = pack

        result = self._run_client_method(method=self.client.rules.get_all,
                                         method_kwargs=kwargs,
                                         format_func=format_result,
                                         format_kwargs={
                                             'exclude_attributes': exclude
                                         })
        return result
