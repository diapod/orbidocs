# Nym-issuance-error.local.v1

Source schema: [`doc/schemas/nym-issuance-error.local.v1.schema.json`](../../schemas/nym-issuance-error.local.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `nym-issuance-error.local.v1` |  |
| [`field`](#field-field) | `yes` | string |  |
| [`reason`](#field-reason) | `yes` | string |  |
| [`authority/reason`](#field-authority-reason) | `no` | string |  |
| [`unlock`](#field-unlock) | `no` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `nym-issuance-error.local.v1`

<a id="field-field"></a>
## `field`

- Required: `yes`
- Shape: string

<a id="field-reason"></a>
## `reason`

- Required: `yes`
- Shape: string

<a id="field-authority-reason"></a>
## `authority/reason`

- Required: `no`
- Shape: string

<a id="field-unlock"></a>
## `unlock`

- Required: `no`
- Shape: object
