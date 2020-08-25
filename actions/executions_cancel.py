from lib.action import St2BaseAction

__all__ = [
    'St2ExecutionsCancel'
]


class St2ExecutionsCancel(St2BaseAction):
    def run(self, ids):
        result = {}
        for i in ids:
            try:
                res = self.client.executions.delete_by_id(instance_id=i)
            except Exception as exc:
                result[i] = '{}'.format(exc)
            else:
                result[i] = res
        return result
