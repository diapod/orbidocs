# Component Trace Read Model V1

Source schema: [`doc/schemas/component-trace-read-model.v1.schema.json`](../../schemas/component-trace-read-model.v1.schema.json)

Bounded offline timeline projection derived from one verified communication-trace recording.

## Governing Basis

- [`doc/project/40-proposals/086-component-communication-observation-and-trace-sessions.md`](../../project/40-proposals/086-component-communication-observation-and-trace-sessions.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `component-trace-read-model.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`recording/id`](#field-recording-id) | `yes` | string |  |
| [`summary`](#field-summary) | `yes` | ref: `#/$defs/summary` |  |
| [`timeline`](#field-timeline) | `yes` | array |  |
| [`schema/path-by-digest`](#field-schema-path-by-digest) | `yes` | object |  |
| [`schema/field-help-by-digest`](#field-schema-field-help-by-digest) | `yes` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`counter`](#def-counter) | integer |  |
| [`digest`](#def-digest) | string |  |
| [`relative-path`](#def-relative-path) | string |  |
| [`schema-field-help`](#def-schema-field-help) | object |  |
| [`summary`](#def-summary) | object |  |
| [`marker`](#def-marker) | object |  |
| [`timeline-item`](#def-timeline-item) | unspecified |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `component-trace-read-model.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-recording-id"></a>
## `recording/id`

- Required: `yes`
- Shape: string

<a id="field-summary"></a>
## `summary`

- Required: `yes`
- Shape: ref: `#/$defs/summary`

<a id="field-timeline"></a>
## `timeline`

- Required: `yes`
- Shape: array

<a id="field-schema-path-by-digest"></a>
## `schema/path-by-digest`

- Required: `yes`
- Shape: object

<a id="field-schema-field-help-by-digest"></a>
## `schema/field-help-by-digest`

- Required: `yes`
- Shape: object

## Definition Semantics

<a id="def-counter"></a>
## `$defs.counter`

- Shape: integer

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-relative-path"></a>
## `$defs.relative-path`

- Shape: string

<a id="def-schema-field-help"></a>
## `$defs.schema-field-help`

- Shape: object

<a id="def-summary"></a>
## `$defs.summary`

- Shape: object

<a id="def-marker"></a>
## `$defs.marker`

- Shape: object

<a id="def-timeline-item"></a>
## `$defs.timeline-item`

- Shape: unspecified
