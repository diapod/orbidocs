# Replication Delta Batch v1

Source schema: [`doc/schemas/replication-delta-batch.v1.schema.json`](../../schemas/replication-delta-batch.v1.schema.json)

Bounded batch of replication candidate facts. Each item remains independently schema-gated and admitted by its domain.

## Governing Basis

- [`doc/project/40-proposals/081-horizontal-protocol-primitives.md`](../../project/40-proposals/081-horizontal-protocol-primitives.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `replication-delta-batch.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`batch/id`](#field-batch-id) | `yes` | string |  |
| [`request/ref`](#field-request-ref) | `yes` | string |  |
| [`dataset/id`](#field-dataset-id) | `yes` | string |  |
| [`items`](#field-items) | `yes` | array |  |
| [`next/cursor`](#field-next-cursor) | `no` | ref: `#/$defs/cursor` |  |
| [`complete`](#field-complete) | `yes` | boolean |  |
| [`batch/digest`](#field-batch-digest) | `yes` | ref: `#/$defs/sha256_digest` |  |
| [`signature`](#field-signature) | `no` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`item`](#def-item) | object |  |
| [`cursor`](#def-cursor) | string |  |
| [`sha256_digest`](#def-sha256-digest) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `replication-delta-batch.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-batch-id"></a>
## `batch/id`

- Required: `yes`
- Shape: string

<a id="field-request-ref"></a>
## `request/ref`

- Required: `yes`
- Shape: string

<a id="field-dataset-id"></a>
## `dataset/id`

- Required: `yes`
- Shape: string

<a id="field-items"></a>
## `items`

- Required: `yes`
- Shape: array

<a id="field-next-cursor"></a>
## `next/cursor`

- Required: `no`
- Shape: ref: `#/$defs/cursor`

<a id="field-complete"></a>
## `complete`

- Required: `yes`
- Shape: boolean

<a id="field-batch-digest"></a>
## `batch/digest`

- Required: `yes`
- Shape: ref: `#/$defs/sha256_digest`

<a id="field-signature"></a>
## `signature`

- Required: `no`
- Shape: object

## Definition Semantics

<a id="def-item"></a>
## `$defs.item`

- Shape: object

<a id="def-cursor"></a>
## `$defs.cursor`

- Shape: string

<a id="def-sha256-digest"></a>
## `$defs.sha256_digest`

- Shape: string
