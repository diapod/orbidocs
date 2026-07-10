# Replication Delta Request v1

Source schema: [`doc/schemas/replication-delta-request.v1.schema.json`](../../schemas/replication-delta-request.v1.schema.json)

Bounded request for a replication delta after an opaque profile-owned cursor.

## Governing Basis

- [`doc/project/40-proposals/081-horizontal-protocol-primitives.md`](../../project/40-proposals/081-horizontal-protocol-primitives.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `replication-delta-request.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`request/id`](#field-request-id) | `yes` | string |  |
| [`dataset/id`](#field-dataset-id) | `yes` | string |  |
| [`known/summary-ref`](#field-known-summary-ref) | `yes` | string |  |
| [`after/cursor`](#field-after-cursor) | `yes` | ref: `#/$defs/cursor` |  |
| [`limits`](#field-limits) | `yes` | object |  |
| [`include/tombstones`](#field-include-tombstones) | `yes` | boolean |  |
| [`causal/context`](#field-causal-context) | `yes` | ref: `causal-context.v1.schema.json` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`cursor`](#def-cursor) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `replication-delta-request.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-request-id"></a>
## `request/id`

- Required: `yes`
- Shape: string

<a id="field-dataset-id"></a>
## `dataset/id`

- Required: `yes`
- Shape: string

<a id="field-known-summary-ref"></a>
## `known/summary-ref`

- Required: `yes`
- Shape: string

<a id="field-after-cursor"></a>
## `after/cursor`

- Required: `yes`
- Shape: ref: `#/$defs/cursor`

<a id="field-limits"></a>
## `limits`

- Required: `yes`
- Shape: object

<a id="field-include-tombstones"></a>
## `include/tombstones`

- Required: `yes`
- Shape: boolean

<a id="field-causal-context"></a>
## `causal/context`

- Required: `yes`
- Shape: ref: `causal-context.v1.schema.json`

## Definition Semantics

<a id="def-cursor"></a>
## `$defs.cursor`

- Shape: string
