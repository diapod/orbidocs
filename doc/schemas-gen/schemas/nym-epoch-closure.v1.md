# Nym-epoch-closure.v1

Source schema: [`doc/schemas/nym-epoch-closure.v1.schema.json`](../../schemas/nym-epoch-closure.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `nym-epoch-closure.v1` |  |
| [`profile/digest`](#field-profile-digest) | `yes` | string |  |
| [`federation/id`](#field-federation-id) | `yes` | string |  |
| [`issuer/id`](#field-issuer-id) | `yes` | string |  |
| [`context/digest`](#field-context-digest) | `yes` | string |  |
| [`epoch`](#field-epoch) | `yes` | integer |  |
| [`epoch/start`](#field-epoch-start) | `yes` | string |  |
| [`epoch/end`](#field-epoch-end) | `yes` | string |  |
| [`status/revision`](#field-status-revision) | `yes` | integer |  |
| [`signature`](#field-signature) | `yes` | object |  |
| [`status/digest`](#field-status-digest) | `yes` | string |  |
| [`closed/at`](#field-closed-at) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `nym-epoch-closure.v1`

<a id="field-profile-digest"></a>
## `profile/digest`

- Required: `yes`
- Shape: string

<a id="field-federation-id"></a>
## `federation/id`

- Required: `yes`
- Shape: string

<a id="field-issuer-id"></a>
## `issuer/id`

- Required: `yes`
- Shape: string

<a id="field-context-digest"></a>
## `context/digest`

- Required: `yes`
- Shape: string

<a id="field-epoch"></a>
## `epoch`

- Required: `yes`
- Shape: integer

<a id="field-epoch-start"></a>
## `epoch/start`

- Required: `yes`
- Shape: string

<a id="field-epoch-end"></a>
## `epoch/end`

- Required: `yes`
- Shape: string

<a id="field-status-revision"></a>
## `status/revision`

- Required: `yes`
- Shape: integer

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: object

<a id="field-status-digest"></a>
## `status/digest`

- Required: `yes`
- Shape: string

<a id="field-closed-at"></a>
## `closed/at`

- Required: `yes`
- Shape: string
