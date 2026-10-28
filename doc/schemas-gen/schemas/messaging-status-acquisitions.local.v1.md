# Messaging Status Acquisition Process Counters

Source schema: [`doc/schemas/messaging-status-acquisitions.local.v1.schema.json`](../../schemas/messaging-status-acquisitions.local.v1.schema.json)

Read-only process epoch counters. A counter is an observation, not a grant or a durable receipt.

## Governing Basis

- [`doc/project/40-proposals/076-limited-messaging-grants-decision.md`](../../project/40-proposals/076-limited-messaging-grants-decision.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `messaging-status-acquisitions.local.v1` |  |
| [`process/epoch`](#field-process-epoch) | `yes` | string |  |
| [`policy`](#field-policy) | `yes` | unspecified |  |
| [`counts`](#field-counts) | `yes` | array |  |
| [`peer-renewal`](#field-peer-renewal) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `messaging-status-acquisitions.local.v1`

<a id="field-process-epoch"></a>
## `process/epoch`

- Required: `yes`
- Shape: string

<a id="field-policy"></a>
## `policy`

- Required: `yes`
- Shape: unspecified

<a id="field-counts"></a>
## `counts`

- Required: `yes`
- Shape: array

<a id="field-peer-renewal"></a>
## `peer-renewal`

- Required: `yes`
- Shape: object
