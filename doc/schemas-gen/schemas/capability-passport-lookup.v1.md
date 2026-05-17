# Capability Passport Lookup v1

Source schema: [`doc/schemas/capability-passport-lookup.v1.schema.json`](../../schemas/capability-passport-lookup.v1.schema.json)

Host-capability request and response contract for selecting an already valid local capability passport.

## Governing Basis

- [`doc/project/40-proposals/060-messaging-middleware.md`](../../project/40-proposals/060-messaging-middleware.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `capability-passport-lookup.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`capability/id`](#field-capability-id) | `yes` | string |  |
| [`required/scope`](#field-required-scope) | `yes` | object |  |
| [`freshness`](#field-freshness) | `no` | object |  |
| [`now`](#field-now) | `no` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`subject_string`](#def-subject-string) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `capability-passport-lookup.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-capability-id"></a>
## `capability/id`

- Required: `yes`
- Shape: string

<a id="field-required-scope"></a>
## `required/scope`

- Required: `yes`
- Shape: object

<a id="field-freshness"></a>
## `freshness`

- Required: `no`
- Shape: object

<a id="field-now"></a>
## `now`

- Required: `no`
- Shape: string

## Definition Semantics

<a id="def-subject-string"></a>
## `$defs.subject_string`

- Shape: string
