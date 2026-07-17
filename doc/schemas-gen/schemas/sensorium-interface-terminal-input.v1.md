# Sensorium Interface Terminal Input v1

Source schema: [`doc/schemas/sensorium-interface-terminal-input.v1.schema.json`](../../schemas/sensorium-interface-terminal-input.v1.schema.json)

Bounded raw PTY bytes. Invoke authority is carried by the enclosing P083 request, never by an operator flag.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-interface-terminal-input.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`terminal/session-ref`](#field-terminal-session-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`bytes/base64`](#field-bytes-base64) | `yes` | string |  |
| [`bytes/sha256`](#field-bytes-sha256) | `yes` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-interface-terminal-input.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-terminal-session-ref"></a>
## `terminal/session-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-bytes-base64"></a>
## `bytes/base64`

- Required: `yes`
- Shape: string

<a id="field-bytes-sha256"></a>
## `bytes/sha256`

- Required: `yes`
- Shape: string

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
