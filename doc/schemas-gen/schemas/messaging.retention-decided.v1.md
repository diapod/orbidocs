# Messaging Retention Decided v1

Source schema: [`doc/schemas/messaging.retention-decided.v1.schema.json`](../../schemas/messaging.retention-decided.v1.schema.json)

Messaging-owned Layer 3 fact recording an explicit message or thread retention decision.

## Governing Basis

- [`doc/project/40-proposals/060-messaging-middleware.md`](../../project/40-proposals/060-messaging-middleware.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `messaging.retention-decided.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`fact/id`](#field-fact-id) | `yes` | string |  |
| [`event/at`](#field-event-at) | `yes` | string |  |
| [`target`](#field-target) | `yes` | object |  |
| [`decision/kind`](#field-decision-kind) | `yes` | enum: `keep-local`, `archive`, `delete`, `exported` |  |
| [`decided/by`](#field-decided-by) | `yes` | string |  |
| [`reason`](#field-reason) | `no` | string |  |
| [`archive/ref`](#field-archive-ref) | `no` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `messaging.retention-decided.v1`

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

<a id="field-decision-kind"></a>
## `decision/kind`

- Required: `yes`
- Shape: enum: `keep-local`, `archive`, `delete`, `exported`

<a id="field-decided-by"></a>
## `decided/by`

- Required: `yes`
- Shape: string

<a id="field-reason"></a>
## `reason`

- Required: `no`
- Shape: string

<a id="field-archive-ref"></a>
## `archive/ref`

- Required: `no`
- Shape: string
