# Nym-renewal-approval.local.v1

Source schema: [`doc/schemas/nym-renewal-approval.local.v1.schema.json`](../../schemas/nym-renewal-approval.local.v1.schema.json)

Operator-local stay-ready intention only. The host derives the owned context and epoch from an accepted certification. No key mint, AD delivery or automatic renewal is authorized by this command.

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`profile/digest`](#field-profile-digest) | `yes` | string |  |
| [`local-passphrase`](#field-local-passphrase) | `no` | string | Local unlock input. Never returned or retained as a response field. |
| [`consent/id`](#field-consent-id) | `yes` | string |  |
| [`certification/id`](#field-certification-id) | `yes` | string |  |
| [`maximum/renewals`](#field-maximum-renewals) | `yes` | integer |  |
## Field Semantics

<a id="field-profile-digest"></a>
## `profile/digest`

- Required: `yes`
- Shape: string

<a id="field-local-passphrase"></a>
## `local-passphrase`

- Required: `no`
- Shape: string

Local unlock input. Never returned or retained as a response field.

<a id="field-consent-id"></a>
## `consent/id`

- Required: `yes`
- Shape: string

<a id="field-certification-id"></a>
## `certification/id`

- Required: `yes`
- Shape: string

<a id="field-maximum-renewals"></a>
## `maximum/renewals`

- Required: `yes`
- Shape: integer
