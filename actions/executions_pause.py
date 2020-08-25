from lib.action import St2BaseAction

__all__ = [
    'St2ExecutionsPause'
]


def format_result(item):
    if not item:
        return None

    return item.to_dict()


class St2ExecutionsPause(St2BaseAction):
    def run(self, ids):
        result = {}
        for i in ids:
            try:
                res = self.client.liveactions.pause(execution_id=id)
            except Exception as exc:
                result[i] = '{}'.format(exc)
            else:
                result[i] = format_result(item=res)
        return result
