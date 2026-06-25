# Capability Authorization Policy v1

Source schema: [`doc/schemas/capability-authorization-policy.v1.schema.json`](../../schemas/capability-authorization-policy.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `capability-authorization-policy.v1` |  |
| [`policy/id`](#field-policy-id) | `yes` | string |  |
| [`registry/ref`](#field-registry-ref) | `yes` | const: `capability-registry.v1` |  |
| [`entries`](#field-entries) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`entry`](#def-entry) | object |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `capability-authorization-policy.v1`

<a id="field-policy-id"></a>
## `policy/id`

- Required: `yes`
- Shape: string

<a id="field-registry-ref"></a>
## `registry/ref`

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
