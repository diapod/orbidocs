# Nym-exchange-key-request.v1

Source schema: [`doc/schemas/nym-exchange-key-request.v1.schema.json`](../../schemas/nym-exchange-key-request.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `nym-exchange-key-request.v1` |  |
| [`issuer/id`](#field-issuer-id) | `yes` | string |  |
| [`profile/digest`](#field-profile-digest) | `yes` | string |  |
| [`applicant/id`](#field-applicant-id) | `yes` | string |  |
| [`exchange/digest`](#field-exchange-digest) | `yes` | string |  |
| [`reply/recipient`](#field-reply-recipient) | `yes` | string |  |
| [`reply/key`](#field-reply-key) | `yes` | string |  |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`expires/at`](#field-expires-at) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `nym-exchange-key-request.v1`

<a id="field-issuer-id"></a>
## `issuer/id`

- Required: `yes`
- Shape: string

<a id="field-profile-digest"></a>
## `profile/digest`

- Required: `yes`
- Shape: string

<a id="field-applicant-id"></a>
## `applicant/id`

- Required: `yes`
- Shape: string

<a id="field-exchange-digest"></a>
## `exchange/digest`

- Required: `yes`
- Shape: string

<a id="field-reply-recipient"></a>
## `reply/recipient`

- Required: `yes`
- Shape: string

<a id="field-reply-key"></a>
## `reply/key`

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
