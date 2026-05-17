# Messaging Crisis Marked v1

Source schema: [`doc/schemas/messaging.crisis-marked.v1.schema.json`](../../schemas/messaging.crisis-marked.v1.schema.json)

Messaging-owned Layer 3 fact recording an explicit user or policy mark that places a message or thread in crisis handling.

## Governing Basis

- [`doc/project/40-proposals/060-messaging-middleware.md`](../../project/40-proposals/060-messaging-middleware.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `messaging.crisis-marked.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`fact/id`](#field-fact-id) | `yes` | string |  |
| [`event/at`](#field-event-at) | `yes` | string |  |
| [`target`](#field-target) | `yes` | object |  |
| [`mark/kind`](#field-mark-kind) | `yes` | enum: `marked`, `cleared` |  |
| [`marked/by`](#field-marked-by) | `yes` | string |  |
| [`reason`](#field-reason) | `no` | string |  |
| [`crisis-space/id`](#field-crisis-space-id) | `no` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `messaging.crisis-marked.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-fact-id"></a>
## `fact/id`

- Required: `yes`
- Shape: string

<a id="field-event-at"></a>
## `event/at`

- Required: `yes`
- Shape: string

<a id="field-target"></a>
## `target`

- Required: `yes`
- Shape: object

<a id="field-mark-kind"></a>
## `mark/kind`

- Required: `yes`
- Shape: enum: `marked`, `cleared`

<a id="field-marked-by"></a>
## `marked/by`

- Required: `yes`
- Shape: string

<a id="field-reason"></a>
## `reason`

- Required: `no`
- Shape: string

<a id="field-crisis-space-id"></a>
## `crisis-space/id`

- Required: `no`
- Shape: string
