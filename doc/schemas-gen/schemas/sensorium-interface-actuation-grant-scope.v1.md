# Sensorium Interface Actuation Grant Scope v1

Source schema: [`doc/schemas/sensorium-interface-actuation-grant-scope.v1.schema.json`](../../schemas/sensorium-interface-actuation-grant-scope.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-interface-actuation-grant-scope.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`interface/id`](#field-interface-id) | `yes` | string |  |
| [`methods`](#field-methods) | `yes` | array |  |
| [`remote/node-ids`](#field-remote-node-ids) | `yes` | array | Additional federated-node restriction. Empty is local-only by admission context, never a federated wildcard. |
| [`classification/max-tier`](#field-classification-max-tier) | `yes` | enum: `Public`, `Community`, `Personal` |  |
| [`limits`](#field-limits) | `yes` | ref: `#/$defs/limits` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`limits`](#def-limits) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-interface-actuation-grant-scope.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-interface-id"></a>
## `interface/id`

- Required: `yes`
- Shape: string

<a id="field-methods"></a>
## `methods`

- Required: `yes`
- Shape: array

<a id="field-remote-node-ids"></a>
## `remote/node-ids`

- Required: `yes`
- Shape: array

Additional federated-node restriction. Empty is local-only by admission context, never a federated wildcard.

<a id="field-classification-max-tier"></a>
## `classification/max-tier`

- Required: `yes`
- Shape: enum: `Public`, `Community`, `Personal`

<a id="field-limits"></a>
## `limits`

- Required: `yes`
- Shape: ref: `#/$defs/limits`

## Definition Semantics

<a id="def-limits"></a>
## `$defs.limits`

- Shape: object
