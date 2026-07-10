# Replication Summary v1

Source schema: [`doc/schemas/replication-summary.v1.schema.json`](../../schemas/replication-summary.v1.schema.json)

Bounded anti-entropy summary for one signed immutable fact dataset.

## Governing Basis

- [`doc/project/40-proposals/081-horizontal-protocol-primitives.md`](../../project/40-proposals/081-horizontal-protocol-primitives.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `replication-summary.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`summary/id`](#field-summary-id) | `yes` | string |  |
| [`dataset/id`](#field-dataset-id) | `yes` | string |  |
| [`dataset/epoch`](#field-dataset-epoch) | `yes` | integer |  |
| [`replication/profile-id`](#field-replication-profile-id) | `yes` | string |  |
| [`source/node-id`](#field-source-node-id) | `yes` | string |  |
| [`federation/id`](#field-federation-id) | `no` | string |  |
| [`high-water/cursor`](#field-high-water-cursor) | `yes` | ref: `#/$defs/cursor` |  |
| [`retention/floor`](#field-retention-floor) | `no` | ref: `#/$defs/cursor` |  |
| [`records/count`](#field-records-count) | `yes` | integer |  |
| [`tombstones/high-water`](#field-tombstones-high-water) | `no` | ref: `#/$defs/cursor` |  |
| [`digest`](#field-digest) | `yes` | ref: `#/$defs/digest_profile` |  |
| [`generated/at`](#field-generated-at) | `yes` | string |  |
| [`expires/at`](#field-expires-at) | `yes` | string |  |
| [`signature`](#field-signature) | `no` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`cursor`](#def-cursor) | string |  |
| [`digest_profile`](#def-digest-profile) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `replication-summary.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-summary-id"></a>
## `summary/id`

- Required: `yes`
- Shape: string

<a id="field-dataset-id"></a>
## `dataset/id`

- Required: `yes`
- Shape: string

<a id="field-dataset-epoch"></a>
## `dataset/epoch`

- Required: `yes`
- Shape: integer

<a id="field-replication-profile-id"></a>
## `replication/profile-id`

- Required: `yes`
- Shape: string

<a id="field-source-node-id"></a>
## `source/node-id`

- Required: `yes`
- Shape: string

<a id="field-federation-id"></a>
## `federation/id`

- Required: `no`
- Shape: string

<a id="field-high-water-cursor"></a>
## `high-water/cursor`

- Required: `yes`
- Shape: ref: `#/$defs/cursor`

<a id="field-retention-floor"></a>
## `retention/floor`

- Required: `no`
- Shape: ref: `#/$defs/cursor`

<a id="field-records-count"></a>
## `records/count`

- Required: `yes`
- Shape: integer

<a id="field-tombstones-high-water"></a>
## `tombstones/high-water`

- Required: `no`
- Shape: ref: `#/$defs/cursor`

<a id="field-digest"></a>
## `digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest_profile`

<a id="field-generated-at"></a>
## `generated/at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires/at`

- Required: `yes`
- Shape: string

<a id="field-signature"></a>
## `signature`

- Required: `no`
- Shape: object

## Definition Semantics

<a id="def-cursor"></a>
## `$defs.cursor`

- Shape: string

<a id="def-digest-profile"></a>
## `$defs.digest_profile`

- Shape: object
