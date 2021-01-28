from lib.action import St2BaseAction

__all__ = [
    'St2ExecutionsCancel'
]


class St2ExecutionsCancel(St2BaseAction):
    def run(self, ids):
        result = {}
        success = True
        for i in ids:
            try:
                res = self.client.executions.delete_by_id(instance_id=i)
                if res.get('faultstring'):
                    success = False
            except Exception as exc:
                result[i] = str(exc)
                success = False
            else:
                result[i] = res
        return success, result
