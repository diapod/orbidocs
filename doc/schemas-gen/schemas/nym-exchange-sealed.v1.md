# Nym-exchange-sealed.v1

Source schema: [`doc/schemas/nym-exchange-sealed.v1.schema.json`](../../schemas/nym-exchange-sealed.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `nym-exchange-sealed.v1` |  |
| [`exchange/digest`](#field-exchange-digest) | `yes` | string |  |
| [`payload/schema`](#field-payload-schema) | `yes` | enum: `nym-issuance-request.v1`, `nym-issuance-decision.v1` |  |
| [`recipient/key-ref`](#field-recipient-key-ref) | `yes` | string |  |
| [`sender/ephemeral-key`](#field-sender-ephemeral-key) | `yes` | string |  |
| [`nonce`](#field-nonce) | `yes` | string |  |
| [`ciphertext`](#field-ciphertext) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `nym-exchange-sealed.v1`

<a id="field-exchange-digest"></a>
## `exchange/digest`

- Required: `yes`
- Shape: string

<a id="field-payload-schema"></a>
## `payload/schema`

- Required: `yes`
- Shape: enum: `nym-issuance-request.v1`, `nym-issuance-decision.v1`

<a id="field-recipient-key-ref"></a>
## `recipient/key-ref`

- Required: `yes`
- Shape: string

<a id="field-sender-ephemeral-key"></a>
## `sender/ephemeral-key`

- Required: `yes`
- Shape: string

<a id="field-nonce"></a>
## `nonce`

- Required: `yes`
- Shape: string

<a id="field-ciphertext"></a>
## `ciphertext`

- Required: `yes`
- Shape: string
