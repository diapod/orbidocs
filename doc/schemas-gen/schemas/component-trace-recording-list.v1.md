# Component Trace Recording List V1

Source schema: [`doc/schemas/component-trace-recording-list.v1.schema.json`](../../schemas/component-trace-recording-list.v1.schema.json)

Bounded operator projection of closed offline communication-trace recordings.

## Governing Basis

- [`doc/project/40-proposals/086-component-communication-observation-and-trace-sessions.md`](../../project/40-proposals/086-component-communication-observation-and-trace-sessions.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `component-trace-recording-list.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`recordings`](#field-recordings) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`timestamp`](#def-timestamp) | string |  |
| [`counter`](#def-counter) | integer |  |
| [`recording`](#def-recording) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `component-trace-recording-list.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-recordings"></a>
## `recordings`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-timestamp"></a>
## `$defs.timestamp`

- Shape: string

<a id="def-counter"></a>
## `$defs.counter`

- Shape: integer

<a id="def-recording"></a>
## `$defs.recording`

- Shape: object
