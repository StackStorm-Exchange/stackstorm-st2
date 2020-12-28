import json

from lib.action import St2BaseAction

__all__ = [
    'St2KVPDeleteEntryPropertyAction'
]


class St2KVPDeleteEntryPropertyAction(St2BaseAction):
    # noinspection PyShadowingBuiltins
    def run(self, key, entry, property):
        # get and deserialize object or fail.
        _key = self.client.keys.get_by_name(key, decrypt=False)

        if not _key:
            raise Exception("Key does not exist in datastore")

        deserialized = json.loads(_key.value)

        # delete object.entry.property
        _entry = deserialized.get(entry, {})
        try:
            del _entry[property]
        except KeyError:
            pass

        # delete object.entry if entry is empty
        if not _entry:
            try:
                del deserialized[entry]
            except KeyError:
                pass

        # re-serialize and save
        serialized = json.dumps(deserialized)
        kvp = self._kvp(name=key, value=serialized)
        kvp.id = key

        self.client.keys.update(kvp)
        response = {
            'key': key,
            'entry_name': entry,
            'entry': _entry,
            'entry_deleted': not _entry,
        }
        return response
