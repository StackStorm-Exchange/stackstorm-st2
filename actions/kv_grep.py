from lib.action import St2BaseAction

__all__ = [
    'St2KVPGrepAction'
]


class St2KVPGrepAction(St2BaseAction):
    def run(self, query, prefix=False):
        if prefix:
            _keys = self.client.keys.get_all(prefix=query)
            results = {key.name: key.value for key in _keys}
        else:
            _keys = self.client.keys.get_all()
            results = {}
            for key in _keys:
                if query in key.name:
                    results[key.name] = key.value
        return results
