# Component Trace Gap V1

Source schema: [`doc/schemas/component-trace-gap.v1.schema.json`](../../schemas/component-trace-gap.v1.schema.json)

Generation-bound evidence that observations are unavailable.

## Governing Basis

- [`doc/project/40-proposals/086-component-communication-observation-and-trace-sessions.md`](../../project/40-proposals/086-component-communication-observation-and-trace-sessions.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `component-trace-gap.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`observation/generation`](#field-observation-generation) | `yes` | ref: `#/$defs/ref` |  |
| [`requested/cursor`](#field-requested-cursor) | `yes` | ref: `#/$defs/cursor` |  |
| [`earliest/available-cursor`](#field-earliest-available-cursor) | `yes` | ref: `#/$defs/cursor` |  |
| [`latest/available-cursor`](#field-latest-available-cursor) | `yes` | ref: `#/$defs/cursor` |  |
| [`known/lost-count`](#field-known-lost-count) | `no` | ref: `#/$defs/cursor` |  |
| [`reason`](#field-reason) | `yes` | enum: `buffer-evicted`, `subscriber-lagged`, `process-restarted`, `recorder-interrupted`, `policy-transition-unavailable`, `context-unavailable` |  |
| [`boundary/filters`](#field-boundary-filters) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`cursor`](#def-cursor) | integer |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `component-trace-gap.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-observation-generation"></a>
## `observation/generation`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-requested-cursor"></a>
## `requested/cursor`

- Required: `yes`
- Shape: ref: `#/$defs/cursor`

<a id="field-earliest-available-cursor"></a>
## `earliest/available-cursor`

- Required: `yes`
- Shape: ref: `#/$defs/cursor`

<a id="field-latest-available-cursor"></a>
## `latest/available-cursor`

- Required: `yes`
- Shape: ref: `#/$defs/cursor`

<a id="field-known-lost-count"></a>
## `known/lost-count`

- Required: `no`
- Shape: ref: `#/$defs/cursor`

<a id="field-reason"></a>
## `reason`

- Required: `yes`
- Shape: enum: `buffer-evicted`, `subscriber-lagged`, `process-restarted`, `recorder-interrupted`, `policy-transition-unavailable`, `context-unavailable`

<a id="field-boundary-filters"></a>
## `boundary/filters`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-cursor"></a>
## `$defs.cursor`

- Shape: integer
