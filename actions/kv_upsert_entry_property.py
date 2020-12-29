import json

from st2common.services import coordination as coordination_service

from lib.action import St2BaseAction

__all__ = [
    'St2KVPUpsertEntryPropertyAction'
]


class St2KVPUpsertEntryPropertyAction(St2BaseAction):
    # noinspection PyShadowingBuiltins
    def run(self, key, entry, property, value):
        with coordination_service.get_coordinator().get_lock('st2.kv_entry.' + key):
            # get and deserialize object or fail.
            _key = self.client.keys.get_by_name(key, decrypt=False)

            if not _key:
                raise Exception("Key does not exist in datastore")

            # optimistically try to decode a json value
            try:
                value = json.loads(value)
            except (TypeError, ValueError):
                # assume it is either already decoded (TypeError)
                # or it is a plain string (ValueError)
                # (malformed JSON objects/arrays will be strings)
                pass

            deserialized = json.loads(_key.value)

            # update or insert object.entry.property
            _entry = deserialized.get(entry, {})
            _entry[property] = value
            deserialized[entry] = _entry

            # re-serialize and save
            serialized = json.dumps(deserialized)
            kvp = self._kvp(name=key, value=serialized)
            kvp.id = key

            self.client.keys.update(kvp)
            response = {
                'key': key,
                'entry_name': entry,
                'entry': _entry,
            }
            return response
