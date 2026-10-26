# Nym-issuance-consent.local.v1

Source schema: [`doc/schemas/nym-issuance-consent.local.v1.schema.json`](../../schemas/nym-issuance-consent.local.v1.schema.json)

Operator-local input. The route identifies the command. It supplies no issuer trust, private key, delivery decision or certificate authority.

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`profile/digest`](#field-profile-digest) | `yes` | string |  |
| [`operation/id`](#field-operation-id) | `yes` | string |  |
| [`local-passphrase`](#field-local-passphrase) | `no` | string | Local unlock input. Never returned or retained as a response field. |
| [`phase`](#field-phase) | `yes` | enum: `key-offer`, `decision` |  |
| [`offer/key`](#field-offer-key) | `yes` | string |  |
| [`notification/id`](#field-notification-id) | `yes` | string |  |
## Field Semantics

<a id="field-profile-digest"></a>
## `profile/digest`

- Required: `yes`
- Shape: string

<a id="field-operation-id"></a>
## `operation/id`

- Required: `yes`
- Shape: string

<a id="field-local-passphrase"></a>
## `local-passphrase`

- Required: `no`
- Shape: string

Local unlock input. Never returned or retained as a response field.

<a id="field-phase"></a>
## `phase`

- Required: `yes`
- Shape: enum: `key-offer`, `decision`

<a id="field-offer-key"></a>
## `offer/key`

- Required: `yes`
- Shape: string

<a id="field-notification-id"></a>
## `notification/id`

- Required: `yes`
- Shape: string
