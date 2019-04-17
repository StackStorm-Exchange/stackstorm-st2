import json

from lib.action import St2BaseAction

__all__ = [
    'St2KVPGrepObjectAction'
]


class St2KVPGrepObjectAction(St2BaseAction):
    def run(self, query, prefix=False):
        if prefix:
            _keys = self.client.keys.get_all(prefix=query)
            results = {}
            for key in _keys:
                results[key.name] = json.loads(key.value)
        else:
            _keys = self.client.keys.get_all()
            results = {}
            for key in _keys:
                if query in key.name:
                    results[key.name] = json.loads(key.value)
        return results
