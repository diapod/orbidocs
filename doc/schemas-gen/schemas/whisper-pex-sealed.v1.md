# Whisper-pex-sealed.v1

Source schema: [`doc/schemas/whisper-pex-sealed.v1.schema.json`](../../schemas/whisper-pex-sealed.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/013-whisper-social-signal-exchange/private-case-continuity.md`](../../project/40-proposals/013-whisper-social-signal-exchange/private-case-continuity.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-pex-sealed.v1` |  |
| [`payload/schema`](#field-payload-schema) | `yes` | enum: `whisper-protected-signal.v1`, `whisper-case-command.v1`, `whisper-case-result.v1` |  |
| [`offer/digest`](#field-offer-digest) | `yes` | string |  |
| [`recipient/key-ref`](#field-recipient-key-ref) | `yes` | string |  |
| [`sender/ephemeral-key`](#field-sender-ephemeral-key) | `yes` | string |  |
| [`nonce`](#field-nonce) | `yes` | string |  |
| [`ciphertext`](#field-ciphertext) | `yes` | string |  |
| [`exchange/handle`](#field-exchange-handle) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-pex-sealed.v1`

<a id="field-payload-schema"></a>
## `payload/schema`

- Required: `yes`
- Shape: enum: `whisper-protected-signal.v1`, `whisper-case-command.v1`, `whisper-case-result.v1`

<a id="field-offer-digest"></a>
## `offer/digest`

- Required: `yes`
- Shape: string

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

<a id="field-exchange-handle"></a>
## `exchange/handle`

- Required: `yes`
- Shape: string
