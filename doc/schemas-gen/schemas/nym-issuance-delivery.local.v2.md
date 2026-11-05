# Nym-issuance-delivery.local.v2

Source schema: [`doc/schemas/nym-issuance-delivery.local.v2.schema.json`](../../schemas/nym-issuance-delivery.local.v2.schema.json)

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `nym-issuance-delivery.local.v2` |  |
| [`operation/id`](#field-operation-id) | `yes` | string |  |
| [`artifact/id`](#field-artifact-id) | `yes` | string |  |
| [`artifact/digest`](#field-artifact-digest) | `yes` | string |  |
| [`delivery/id`](#field-delivery-id) | `yes` | string |  |
| [`delivery/state`](#field-delivery-state) | `yes` | enum: `accepted`, `running`, `succeeded`, `partial`, `failed-retryable`, `failed-permanent`, `expired` |  |
| [`issuance`](#field-issuance) | `yes` | ref: `nym-issuance-readback.local.v2.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `nym-issuance-delivery.local.v2`

<a id="field-operation-id"></a>
## `operation/id`

- Required: `yes`
- Shape: string

<a id="field-artifact-id"></a>
## `artifact/id`

- Required: `yes`
- Shape: string

<a id="field-artifact-digest"></a>
## `artifact/digest`

- Required: `yes`
- Shape: string

<a id="field-delivery-id"></a>
## `delivery/id`

- Required: `yes`
- Shape: string

<a id="field-delivery-state"></a>
## `delivery/state`

- Required: `yes`
- Shape: enum: `accepted`, `running`, `succeeded`, `partial`, `failed-retryable`, `failed-permanent`, `expired`

<a id="field-issuance"></a>
## `issuance`

- Required: `yes`
- Shape: ref: `nym-issuance-readback.local.v2.schema.json`
