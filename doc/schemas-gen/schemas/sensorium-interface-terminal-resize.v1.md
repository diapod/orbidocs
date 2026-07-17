# Sensorium Interface Terminal Resize v1

Source schema: [`doc/schemas/sensorium-interface-terminal-resize.v1.schema.json`](../../schemas/sensorium-interface-terminal-resize.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-interface-terminal-resize.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`terminal/session-ref`](#field-terminal-session-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`rows`](#field-rows) | `yes` | integer |  |
| [`cols`](#field-cols) | `yes` | integer |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-interface-terminal-resize.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-terminal-session-ref"></a>
## `terminal/session-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-rows"></a>
## `rows`

- Required: `yes`
- Shape: integer

<a id="field-cols"></a>
## `cols`

- Required: `yes`
- Shape: integer

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
