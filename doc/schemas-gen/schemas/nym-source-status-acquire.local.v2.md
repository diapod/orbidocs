# Nym-source-status-acquire.local.v2

Source schema: [`doc/schemas/nym-source-status-acquire.local.v2.schema.json`](../../schemas/nym-source-status-acquire.local.v2.schema.json)

Bounded status acquisition for an independently adopted v3 profile and exact v3 certificate. No caller clock, endpoint, profile adoption, key or issuance authority.

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`profile/digest`](#field-profile-digest) | `yes` | string |  |
| [`certificate`](#field-certificate) | `yes` | ref: `whisper-source-certificate.v3.schema.json` |  |
| [`purpose`](#field-purpose) | `yes` | enum: `collection`, `first-emission` |  |
## Field Semantics

<a id="field-profile-digest"></a>
## `profile/digest`

- Required: `yes`
- Shape: string

<a id="field-certificate"></a>
## `certificate`

- Required: `yes`
- Shape: ref: `whisper-source-certificate.v3.schema.json`

<a id="field-purpose"></a>
## `purpose`

- Required: `yes`
- Shape: enum: `collection`, `first-emission`
