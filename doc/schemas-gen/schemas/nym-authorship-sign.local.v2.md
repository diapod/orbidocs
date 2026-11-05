# Nym-authorship-sign.local.v2

Source schema: [`doc/schemas/nym-authorship-sign.local.v2.schema.json`](../../schemas/nym-authorship-sign.local.v2.schema.json)

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
| [`preview/digest`](#field-preview-digest) | `yes` | string |  |
| [`review/ref`](#field-review-ref) | `yes` | string |  |
| [`review/digest`](#field-review-digest) | `yes` | string |  |
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

<a id="field-preview-digest"></a>
## `preview/digest`

- Required: `yes`
- Shape: string

<a id="field-review-ref"></a>
## `review/ref`

- Required: `yes`
- Shape: string

<a id="field-review-digest"></a>
## `review/digest`

- Required: `yes`
- Shape: string
