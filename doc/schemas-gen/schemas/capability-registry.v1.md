# Capability Registry v1

Source schema: [`doc/schemas/capability-registry.v1.schema.json`](../../schemas/capability-registry.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `capability-registry.v1` |  |
| [`entries`](#field-entries) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`entry`](#def-entry) | object |  |
| [`flags`](#def-flags) | object |  |
| [`docs`](#def-docs) | object |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `capability-registry.v1`

<a id="field-entries"></a>
## `entries`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-entry"></a>
## `$defs.entry`

- Shape: object

<a id="def-flags"></a>
## `$defs.flags`

- Shape: object

<a id="def-docs"></a>
## `$defs.docs`

- Shape: object
