# Sensorium Interface Terminal Signal v1

Source schema: [`doc/schemas/sensorium-interface-terminal-signal.v1.schema.json`](../../schemas/sensorium-interface-terminal-signal.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-interface-terminal-signal.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`terminal/session-ref`](#field-terminal-session-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`signal`](#field-signal) | `yes` | enum: `TERM`, `INT`, `KILL`, `STOP`, `CONT` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-interface-terminal-signal.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-terminal-session-ref"></a>
## `terminal/session-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-signal"></a>
## `signal`

- Required: `yes`
- Shape: enum: `TERM`, `INT`, `KILL`, `STOP`, `CONT`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
