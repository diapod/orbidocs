# Middleware Channel Request Cancel v1

Source schema: [`doc/schemas/middleware-channel-request-cancel.v1.schema.json`](../../schemas/middleware-channel-request-cancel.v1.schema.json)

Best-effort cancellation request bound to one request previously initiated by the control sender.

## Governing Basis

- [`doc/project/40-proposals/080-multiplexed-middleware-channel-executor.md`](../../project/40-proposals/080-multiplexed-middleware-channel-executor.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `middleware-channel-request-cancel.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`cancel/target`](#field-cancel-target) | `yes` | ref: `#/$defs/id` |  |
| [`reason`](#field-reason) | `yes` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`id`](#def-id) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `middleware-channel-request-cancel.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-cancel-target"></a>
## `cancel/target`

- Required: `yes`
- Shape: ref: `#/$defs/id`

<a id="field-reason"></a>
## `reason`

- Required: `yes`
- Shape: string

## Definition Semantics

<a id="def-id"></a>
## `$defs.id`

- Shape: string
