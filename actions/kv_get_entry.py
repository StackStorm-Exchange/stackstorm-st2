import json

from lib.action import St2BaseAction

__all__ = [
    'St2KVPGetEntryAction'
]


class St2KVPGetEntryAction(St2BaseAction):
    # noinspection PyShadowingBuiltins
    def run(self, key, fallback, entry):
        # get and deserialize object or fail.
        _key = self.client.keys.get_by_name(key, decrypt=False)

        if not _key:
            raise Exception("Key does not exist in datastore")

        deserialized = json.loads(_key.value)

        # try get object.entry.property
        _entry = deserialized.get(fallback, {})
        _entry.update(deserialized.get(entry, {}))

        return _entry
