# Nym-bootstrap-recipient.v1

Source schema: [`doc/schemas/nym-bootstrap-recipient.v1.schema.json`](../../schemas/nym-bootstrap-recipient.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `nym-bootstrap-recipient.v1` |  |
| [`issuer/id`](#field-issuer-id) | `yes` | string |  |
| [`profile/digest`](#field-profile-digest) | `yes` | string |  |
| [`recipient/node-id`](#field-recipient-node-id) | `yes` | string |  |
| [`purpose`](#field-purpose) | `yes` | const: `nym-exchange-key-request.v1` |  |
| [`recipient/key`](#field-recipient-key) | `yes` | string |  |
| [`recipient/key-ref`](#field-recipient-key-ref) | `yes` | string |  |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`expires/at`](#field-expires-at) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `nym-bootstrap-recipient.v1`

<a id="field-issuer-id"></a>
## `issuer/id`

- Required: `yes`
- Shape: string

<a id="field-profile-digest"></a>
## `profile/digest`

- Required: `yes`
- Shape: string

<a id="field-recipient-node-id"></a>
## `recipient/node-id`

- Required: `yes`
- Shape: string

<a id="field-purpose"></a>
## `purpose`

- Required: `yes`
- Shape: const: `nym-exchange-key-request.v1`

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
