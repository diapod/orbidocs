# Agora-publication-receipt.local.v1

Source schema: [`doc/schemas/agora-publication-receipt.local.v1.schema.json`](../../schemas/agora-publication-receipt.local.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agora-publication-receipt.local.v1` |  |
| [`record/id`](#field-record-id) | `yes` | string |  |
| [`author/bytes-digest`](#field-author-bytes-digest) | `yes` | string |  |
| [`clock/authority`](#field-clock-authority) | `yes` | string |  |
| [`accepted/at`](#field-accepted-at) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agora-publication-receipt.local.v1`

<a id="field-record-id"></a>
## `record/id`

- Required: `yes`
- Shape: string

<a id="field-author-bytes-digest"></a>
## `author/bytes-digest`

- Required: `yes`
- Shape: string

<a id="field-clock-authority"></a>
## `clock/authority`

- Required: `yes`
- Shape: string

<a id="field-accepted-at"></a>
## `accepted/at`

- Required: `yes`
- Shape: string

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: object
