# StackStorm Integration Pack

The super-meta package! This integration allows integration with StackStorm.

Requires StackStorm >= `v0.8.0`

## Configuration:

Copy the example configuration in [st2.yaml.example](./st2.yaml.example)
to `/opt/stackstorm/configs/st2.yaml` and edit as required.

* `base_url` - Base URL for the StackStorm API server endpoints (i.e.
  ``http://localhost``). If only the base URL is provided, the client will
  assume default ports for the API servers are used. If any of the API server
  URL is provided, it will override the base URL and default port. If no value
  is provided will assume the pack is expected to work with current StackStorm
  instance and pick up appropriate values from the actions environment. See
  http://docs.stackstorm.com/actions.html#common-environment-variables-available-to-the-actions
* `api_url` - Base API url for the StackStorm API Server endpoint. (e.g.: https://localhost/api)
* `auth_url` - Base AUTH url for the StackStorm Auth Server endpoint. (e.g.: https://localhost/auth)
* `api_key` - API key used to authenticate against the StackStorm API.

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

**Note** : When modifying the configuration in `/opt/stackstorm/configs/` please
           remember to tell StackStorm to load these new values by running
           `st2ctl reload --register-configs`

## Actions

### Datastore

* ``kv.get`` - Retrieve string value from a datastore.
* ``kv.set`` - Store string value in a datastore.
* ``kv.grep`` - Find datastore items which name matches the provided query.
* ``kv.delete`` - Delete item from a datastore.

* ``kv.get_object`` - Deserialize and retrieve JSON serialized object from a
  datastore.
* ``kv.set_object`` - Serialize and store object in a datastore. Note: object
  is serialized as JSON.
* ``kv.grep_object`` - Find datastore items which name matches the provided query
  amd deserialize their values from JSON serialized objects.

Note: ``kv.set`` and ``kv.get`` actions support compressing value before
storing it in a datastore and decompressing it when retrieving it from
a datastore.

If you want data to be compressed, you should pass ``compress=True``
parameter to the ``kv.set`` action when storing a value and ``decompress=True``
when retrieving it.

Values are compressed using bzip2. Keep in mind that values are base64 encoded
after compression which adds around 40% of overhead to the compressed value
size. For typical large strings this should still result in a reduction of
a total size by 40-60% on average.

## ChatOps commands

By default, this pack also includes ChatOps commands (aliases) which allow you
to query your StackStorm installation for things such as available actions,
sensors and more.

* ``!st2 list actions [pack=<pack name>]`` - List available StackStorm actions.
* ``!st2 list rules`` - List available StackStorm rules.
* ``!st2 list sensors [pack=<pack name>]`` - List available StackStorm sensors.
* ``!st2 list executions [action=<action name>] [status=<status>]`` - View a
  history of action executions.
* ``!st2 executions get <execution id>`` - View details for a particular
  action execution.
* ``!st2 executions re-run <execution id>`` - Re-run a particular action
  execution.
