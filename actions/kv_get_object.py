import json
import bz2
import base64
from lib.action import St2BaseAction

__all__ = [
    'St2KVPGetObjectAction'
]


class St2KVPGetObjectAction(St2BaseAction):
    def run(self, key, decompress=False, decrypt=False):
        _key = self.client.keys.get_by_name(key, decrypt=decrypt)

        if not _key:
            raise Exception("Key does not exist")

        if decompress:
            value = base64.b64decode(_key.value)
            value = bz2.decompress(value)
        else:
            value = _key.value

        deserialized_value = json.loads(value)
        return deserialized_value
