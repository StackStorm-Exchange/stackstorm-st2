# Change Log

## 1.2.0

- Added `st2.executions.pause`, `st2.executions.resume`, `st2.executions.cancel` actions.

## 1.1.0

- Added decrypt and decompress parameters to `st2.kv.get_object`
- Fixed cacert=True case in pack's configuration

## 1.0.7

- Added executions.create action that allows a workflow to run another action asynchronously.
  This enables running sub-workflows concurrently and tracking their execution ids.

## 1.0.6

- Add `executions.get_root` action

## 1.0.5

- Added a new option `prefix` to the `st2.kv.grep` action allowing more efficient querying 
  of the key/value store if the user is looking for all keys that start with a given query.
  
- Added a new action `st2.kv.grep_object` that greps keys from the k/v store and parses
  serialized JSON data in each value into objects.

## 1.0.4

- Added default to decrypt param for `st2.kv.get` to fix bug

## 1.0.3

- Added the option to decrypt a secret for `st2.kv.get`

## 1.0.2

- Fixed description for `st2.kv.grep` action

## 0.3.0

- Updated action `runner_type` from `run-python` to `python-script`

## 0.2.1

- Changed `cacert` option in `config.schema.yaml` to be string, not boolean

## 0.2.0

- Rename `config.yaml` to `config.schema.yaml` and update to use schema.
