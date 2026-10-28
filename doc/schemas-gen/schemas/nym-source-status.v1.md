# Nym-source-status.v1

Source schema: [`doc/schemas/nym-source-status.v1.schema.json`](../../schemas/nym-source-status.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `nym-source-status.v1` |  |
| [`profile/digest`](#field-profile-digest) | `yes` | string |  |
| [`federation/id`](#field-federation-id) | `yes` | string |  |
| [`issuer/id`](#field-issuer-id) | `yes` | string |  |
| [`context/digest`](#field-context-digest) | `yes` | string |  |
| [`epoch`](#field-epoch) | `yes` | integer |  |
| [`epoch/start`](#field-epoch-start) | `yes` | string |  |
| [`epoch/end`](#field-epoch-end) | `yes` | string |  |
| [`status/revision`](#field-status-revision) | `yes` | integer |  |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`expires/at`](#field-expires-at) | `yes` | string |  |
| [`revoked/sources`](#field-revoked-sources) | `yes` | array |  |
| [`revoked/certificates`](#field-revoked-certificates) | `yes` | array |  |
| [`signature`](#field-signature) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `nym-source-status.v1`

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

<a id="field-issued-at"></a>
## `issued/at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires/at`

- Required: `yes`
- Shape: string

<a id="field-revoked-sources"></a>
## `revoked/sources`

- Required: `yes`
- Shape: array

<a id="field-revoked-certificates"></a>
## `revoked/certificates`

- Required: `yes`
- Shape: array

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: object
