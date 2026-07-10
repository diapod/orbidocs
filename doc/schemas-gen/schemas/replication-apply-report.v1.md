# Replication Apply Report v1

Source schema: [`doc/schemas/replication-apply-report.v1.schema.json`](../../schemas/replication-apply-report.v1.schema.json)

Redacted bounded apply report for a replication batch.

## Governing Basis

- [`doc/project/40-proposals/081-horizontal-protocol-primitives.md`](../../project/40-proposals/081-horizontal-protocol-primitives.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `replication-apply-report.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`report/id`](#field-report-id) | `yes` | string |  |
| [`batch/ref`](#field-batch-ref) | `yes` | string |  |
| [`outcomes`](#field-outcomes) | `yes` | object |  |
| [`refusals`](#field-refusals) | `no` | array |  |
| [`accepted/cursor`](#field-accepted-cursor) | `no` | ref: `#/$defs/cursor` |  |
| [`retry/advice`](#field-retry-advice) | `no` | ref: `#/$defs/retry_advice` |  |
| [`recorded/at`](#field-recorded-at) | `yes` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`cursor`](#def-cursor) | string |  |
| [`retry_advice`](#def-retry-advice) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `replication-apply-report.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-report-id"></a>
## `report/id`

- Required: `yes`
- Shape: string

<a id="field-batch-ref"></a>
## `batch/ref`

- Required: `yes`
- Shape: string

<a id="field-outcomes"></a>
## `outcomes`

- Required: `yes`
- Shape: object

<a id="field-refusals"></a>
## `refusals`

- Required: `no`
- Shape: array

<a id="field-accepted-cursor"></a>
## `accepted/cursor`

- Required: `no`
- Shape: ref: `#/$defs/cursor`

<a id="field-retry-advice"></a>
## `retry/advice`

- Required: `no`
- Shape: ref: `#/$defs/retry_advice`

<a id="field-recorded-at"></a>
## `recorded/at`

- Required: `yes`
- Shape: string

## Definition Semantics

<a id="def-cursor"></a>
## `$defs.cursor`

- Shape: string

<a id="def-retry-advice"></a>
## `$defs.retry_advice`

- Shape: object
