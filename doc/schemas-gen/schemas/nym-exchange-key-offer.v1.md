# Nym Exchange Key Offer v1

Source schema: [`doc/schemas/nym-exchange-key-offer.v1.schema.json`](../../schemas/nym-exchange-key-offer.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `nym-exchange-key-offer.v1` |  |
| [`issuer/id`](#field-issuer-id) | `yes` | string |  |
| [`requester/id`](#field-requester-id) | `yes` | string |  |
| [`exchange/digest`](#field-exchange-digest) | `yes` | string |  |
| [`recipient/key`](#field-recipient-key) | `yes` | string |  |
| [`recipient/key-ref`](#field-recipient-key-ref) | `yes` | string |  |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`expires/at`](#field-expires-at) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `nym-exchange-key-offer.v1`

<a id="field-issuer-id"></a>
## `issuer/id`

- Required: `yes`
- Shape: string

<a id="field-requester-id"></a>
## `requester/id`

- Required: `yes`
- Shape: string

<a id="field-exchange-digest"></a>
## `exchange/digest`

- Required: `yes`
- Shape: string

<a id="field-recipient-key"></a>
## `recipient/key`

- Required: `yes`
- Shape: string

<a id="field-recipient-key-ref"></a>
## `recipient/key-ref`

- Required: `yes`
- Shape: string

<a id="field-issued-at"></a>
## `issued/at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires/at`

- Required: `yes`
- Shape: string

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: object
