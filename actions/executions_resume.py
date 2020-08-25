from lib.action import St2BaseAction
from lib.formatters import format_result

__all__ = [
    'St2ExecutionsResume'
]


class St2ExecutionsResume(St2BaseAction):
    def run(self, ids):
        result = {}
        success = True
        for i in ids:
            try:
                res = self.client.liveactions.resume(execution_id=i)
            except Exception as exc:
                result[i] = str(exc)
                success = False
            else:
                result[i] = format_result(item=res)
        return success, result
