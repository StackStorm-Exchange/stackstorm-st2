from lib.action import St2BaseAction

__all__ = [
    'St2ExecutionsResume'
]


def format_result(item):
    if not item:
        return None

    return item.to_dict()


class St2ExecutionsResume(St2BaseAction):
    def run(self, ids):
        result = {}
        for i in ids:
            try:
                res = self.client.liveactions.resume(execution_id=i)
            except Exception as exc:
                result[i] = '{}'.format(exc)
            else:
                result[i] = format_result(item=res)
        return result
