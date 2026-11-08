# Whisper-pex-key-offer.v1

Source schema: [`doc/schemas/whisper-pex-key-offer.v1.schema.json`](../../schemas/whisper-pex-key-offer.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/013-whisper-social-signal-exchange/private-case-continuity.md`](../../project/40-proposals/013-whisper-social-signal-exchange/private-case-continuity.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-pex-key-offer.v1` |  |
| [`purpose`](#field-purpose) | `yes` | const: `whisper-pex` |  |
| [`recipient/id`](#field-recipient-id) | `yes` | string |  |
| [`recipient/role`](#field-recipient-role) | `yes` | enum: `protected-signal-custodian`, `case-authority`, `case-applicant` |  |
| [`sender/id`](#field-sender-id) | `yes` | string |  |
| [`exchange/handle`](#field-exchange-handle) | `yes` | string |  |
| [`payload/schema`](#field-payload-schema) | `yes` | enum: `whisper-protected-signal.v1`, `whisper-case-command.v1`, `whisper-case-result.v1` |  |
| [`recipient/key`](#field-recipient-key) | `yes` | string |  |
| [`recipient/key-ref`](#field-recipient-key-ref) | `yes` | string |  |
| [`reply/key`](#field-reply-key) | `yes` | string |  |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`expires/at`](#field-expires-at) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-pex-key-offer.v1`

<a id="field-purpose"></a>
## `purpose`

- Required: `yes`
- Shape: const: `whisper-pex`

<a id="field-recipient-id"></a>
## `recipient/id`

- Required: `yes`
- Shape: string

<a id="field-recipient-role"></a>
## `recipient/role`

- Required: `yes`
- Shape: enum: `protected-signal-custodian`, `case-authority`, `case-applicant`

<a id="field-sender-id"></a>
## `sender/id`

- Required: `yes`
- Shape: string

<a id="field-exchange-handle"></a>
## `exchange/handle`

- Required: `yes`
- Shape: string

<a id="field-payload-schema"></a>
## `payload/schema`

- Required: `yes`
- Shape: enum: `whisper-protected-signal.v1`, `whisper-case-command.v1`, `whisper-case-result.v1`

<a id="field-recipient-key"></a>
## `recipient/key`

- Required: `yes`
- Shape: string

<a id="field-recipient-key-ref"></a>
## `recipient/key-ref`

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
