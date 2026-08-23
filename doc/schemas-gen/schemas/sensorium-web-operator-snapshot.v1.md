# Sensorium Web Operator Snapshot v1

Source schema: [`doc/schemas/sensorium-web-operator-snapshot.v1.schema.json`](../../schemas/sensorium-web-operator-snapshot.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-web-operator-snapshot.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`generated/at`](#field-generated-at) | `yes` | string |  |
| [`status`](#field-status) | `yes` | enum: `ready`, `degraded`, `unavailable` |  |
| [`sources`](#field-sources) | `yes` | array |  |
| [`counters`](#field-counters) | `yes` | object |  |
| [`limits`](#field-limits) | `yes` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`digest`](#def-digest) | string |  |
| [`ref`](#def-ref) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-web-operator-snapshot.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-generated-at"></a>
## `generated/at`

- Required: `yes`
- Shape: string

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `ready`, `degraded`, `unavailable`

<a id="field-sources"></a>
## `sources`

- Required: `yes`
- Shape: array

<a id="field-counters"></a>
## `counters`

- Required: `yes`
- Shape: object

<a id="field-limits"></a>
## `limits`

- Required: `yes`
- Shape: object

## Definition Semantics

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
