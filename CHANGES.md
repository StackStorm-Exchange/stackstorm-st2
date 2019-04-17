# Change Log

## 1.0.5

- Added a new option `prefix` to the `st2.kv.grep` action allowing more efficient querying 
  of the key/value store if the user is looking for all keys that start with a given query.

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
