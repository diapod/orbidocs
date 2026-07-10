# Trace Link v1

Source schema: [`doc/schemas/trace-link.v1.schema.json`](../../schemas/trace-link.v1.schema.json)

P074 read-model edge between two normalized trace events.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `trace-link.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`from/event-id`](#field-from-event-id) | `yes` | ref: `#/$defs/event_id` |  |
| [`to/event-id`](#field-to-event-id) | `yes` | ref: `#/$defs/event_id` |  |
| [`relation`](#field-relation) | `yes` | enum: `caused-by`, `continued-by`, `parent-of` |  |
| [`confidence`](#field-confidence) | `yes` | enum: `strong`, `medium`, `weak` |  |
| [`basis`](#field-basis) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`event_id`](#def-event-id) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `trace-link.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-from-event-id"></a>
## `from/event-id`

- Required: `yes`
- Shape: ref: `#/$defs/event_id`

<a id="field-to-event-id"></a>
## `to/event-id`

- Required: `yes`
- Shape: ref: `#/$defs/event_id`

<a id="field-relation"></a>
## `relation`

- Required: `yes`
- Shape: enum: `caused-by`, `continued-by`, `parent-of`

<a id="field-confidence"></a>
## `confidence`

- Required: `yes`
- Shape: enum: `strong`, `medium`, `weak`

<a id="field-basis"></a>
## `basis`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-event-id"></a>
## `$defs.event_id`

- Shape: string
