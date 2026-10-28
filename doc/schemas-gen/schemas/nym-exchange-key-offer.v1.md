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
| [`recipient/key`](#field-recipient-key) | `yes` | string |  |
| [`recipient/key-ref`](#field-recipient-key-ref) | `yes` | string |  |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`expires/at`](#field-expires-at) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | object |  |
| [`exchange/handle`](#field-exchange-handle) | `yes` | string | Independent opaque 256-bit transport correlation; never the private signed request digest. |
| [`bootstrap/key-public`](#field-bootstrap-key-public) | `yes` | string | Domain-separated ephemeral Ed25519 bootstrap proof key; not the participant or nym public key. |
| [`profile/digest`](#field-profile-digest) | `yes` | string |  |
| [`bootstrap/request-digest`](#field-bootstrap-request-digest) | `yes` | string | Digest of the anonymous ephemeral-proof key request, never the domain issuance request. |
| [`reply/key`](#field-reply-key) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `nym-exchange-key-offer.v1`

<a id="field-issuer-id"></a>
## `issuer/id`

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

<a id="field-exchange-handle"></a>
## `exchange/handle`

- Required: `yes`
- Shape: string

Independent opaque 256-bit transport correlation; never the private signed request digest.

<a id="field-bootstrap-key-public"></a>
## `bootstrap/key-public`

- Required: `yes`
- Shape: string

Domain-separated ephemeral Ed25519 bootstrap proof key; not the participant or nym public key.

<a id="field-profile-digest"></a>
## `profile/digest`

- Required: `yes`
- Shape: string

<a id="field-bootstrap-request-digest"></a>
## `bootstrap/request-digest`

- Required: `yes`
- Shape: string

Digest of the anonymous ephemeral-proof key request, never the domain issuance request.

<a id="field-reply-key"></a>
## `reply/key`

- Required: `yes`
- Shape: string
