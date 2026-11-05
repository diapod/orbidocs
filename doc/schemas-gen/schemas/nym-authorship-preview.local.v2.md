# Nym-authorship-preview.local.v2

Source schema: [`doc/schemas/nym-authorship-preview.local.v2.schema.json`](../../schemas/nym-authorship-preview.local.v2.schema.json)

Resolve the exact current common Harvester review in the protected host. Caller cannot replace approved text, origin, claims or author class. Preview refuses custody shorter than document validity; it never clips document expiry to a private horizon.

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`profile/digest`](#field-profile-digest) | `yes` | string |  |
| [`operation/id`](#field-operation-id) | `yes` | string |  |
| [`certification/id`](#field-certification-id) | `yes` | string |  |
| [`local-passphrase`](#field-local-passphrase) | `no` | string |  |
| [`case`](#field-case) | `no` | object |  |
| [`review/ref`](#field-review-ref) | `yes` | string |  |
| [`review/digest`](#field-review-digest) | `yes` | string |  |
| [`publication`](#field-publication) | `yes` | object |  |
## Field Semantics

<a id="field-profile-digest"></a>
## `profile/digest`

- Required: `yes`
- Shape: string

<a id="field-operation-id"></a>
## `operation/id`

- Required: `yes`
- Shape: string

<a id="field-certification-id"></a>
## `certification/id`

- Required: `yes`
- Shape: string

<a id="field-local-passphrase"></a>
## `local-passphrase`

- Required: `no`
- Shape: string

<a id="field-case"></a>
## `case`

- Required: `no`
- Shape: object

<a id="field-review-ref"></a>
## `review/ref`

- Required: `yes`
- Shape: string

<a id="field-review-digest"></a>
## `review/digest`

- Required: `yes`
- Shape: string

<a id="field-publication"></a>
## `publication`

- Required: `yes`
- Shape: object
