# Sensorium Web Refresh Sweep v1

Source schema: [`doc/schemas/sensorium-web-refresh-sweep.v1.schema.json`](../../schemas/sensorium-web-refresh-sweep.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-web-refresh-sweep.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`seen`](#field-seen) | `yes` | integer |  |
| [`launched`](#field-launched) | `yes` | integer |  |
| [`skipped`](#field-skipped) | `yes` | integer |  |
| [`outcomes`](#field-outcomes) | `yes` | array |  |
| [`stop/reason`](#field-stop-reason) | `no` | enum: `idle`, `launch-budget-exhausted`, `shutdown-requested`, `batch-limit-reached`, `connector-unavailable`, `queue-capacity-reached`, `worker-stopped` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-web-refresh-sweep.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-seen"></a>
## `seen`

- Required: `yes`
- Shape: integer

<a id="field-launched"></a>
## `launched`

- Required: `yes`
- Shape: integer

<a id="field-skipped"></a>
## `skipped`

- Required: `yes`
- Shape: integer

<a id="field-outcomes"></a>
## `outcomes`

- Required: `yes`
- Shape: array

<a id="field-stop-reason"></a>
## `stop/reason`

- Required: `no`
- Shape: enum: `idle`, `launch-budget-exhausted`, `shutdown-requested`, `batch-limit-reached`, `connector-unavailable`, `queue-capacity-reached`, `worker-stopped`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
