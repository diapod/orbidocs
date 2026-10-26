# Nym-issuance-consent-result.local.v1

Source schema: [`doc/schemas/nym-issuance-consent-result.local.v1.schema.json`](../../schemas/nym-issuance-consent-result.local.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `nym-issuance-consent-result.local.v1` |  |
| [`operation/id`](#field-operation-id) | `yes` | string |  |
| [`state`](#field-state) | `yes` | const: `invitation-accepted` |  |
| [`offer/key`](#field-offer-key) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `nym-issuance-consent-result.local.v1`

<a id="field-operation-id"></a>
## `operation/id`

- Required: `yes`
- Shape: string

<a id="field-state"></a>
## `state`

- Required: `yes`
- Shape: const: `invitation-accepted`

<a id="field-offer-key"></a>
## `offer/key`

- Required: `yes`
- Shape: string
