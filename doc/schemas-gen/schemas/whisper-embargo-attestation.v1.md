# Whisper-embargo-attestation.v1

Source schema: [`doc/schemas/whisper-embargo-attestation.v1.schema.json`](../../schemas/whisper-embargo-attestation.v1.schema.json)

Private single-audience threshold proposal for the named executor. It binds the exact retained consent and the opaque live trigger. Carries no counts, inventory, revisions, payload or commit authority.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-embargo-attestation.v1` |  |
| [`case/anchor`](#field-case-anchor) | `yes` | string |  |
| [`case/authority`](#field-case-authority) | `yes` | string |  |
| [`condition/original`](#field-condition-original) | `yes` | string |  |
| [`release/id`](#field-release-id) | `yes` | string |  |
| [`manifest/digest`](#field-manifest-digest) | `yes` | string |  |
| [`executor`](#field-executor) | `yes` | string |  |
| [`mode`](#field-mode) | `yes` | enum: `confirm`, `preauthorized` |  |
| [`epoch`](#field-epoch) | `yes` | integer |  |
| [`counting/basis`](#field-counting-basis) | `yes` | enum: `author-epoch-exact`, `later-epoch-conservative` |  |
| [`trigger/digest`](#field-trigger-digest) | `yes` | string |  |
| [`source/as-of`](#field-source-as-of) | `yes` | string |  |
| [`evaluated/at`](#field-evaluated-at) | `yes` | string |  |
| [`valid/until`](#field-valid-until) | `yes` | string |  |
| [`result`](#field-result) | `yes` | const: `threshold-met` |  |
| [`signature`](#field-signature) | `yes` | string |  |
| [`release/not-after`](#field-release-not-after) | `yes` | string |  |
| [`request/digest`](#field-request-digest) | `no` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-embargo-attestation.v1`

<a id="field-case-anchor"></a>
## `case/anchor`

- Required: `yes`
- Shape: string

<a id="field-case-authority"></a>
## `case/authority`

- Required: `yes`
- Shape: string

<a id="field-condition-original"></a>
## `condition/original`

- Required: `yes`
- Shape: string

<a id="field-release-id"></a>
## `release/id`

- Required: `yes`
- Shape: string

<a id="field-manifest-digest"></a>
## `manifest/digest`

- Required: `yes`
- Shape: string

<a id="field-executor"></a>
## `executor`

- Required: `yes`
- Shape: string

<a id="field-mode"></a>
## `mode`

- Required: `yes`
- Shape: enum: `confirm`, `preauthorized`

<a id="field-epoch"></a>
## `epoch`

- Required: `yes`
- Shape: integer

<a id="field-counting-basis"></a>
## `counting/basis`

- Required: `yes`
- Shape: enum: `author-epoch-exact`, `later-epoch-conservative`

<a id="field-trigger-digest"></a>
## `trigger/digest`

- Required: `yes`
- Shape: string

<a id="field-source-as-of"></a>
## `source/as-of`

- Required: `yes`
- Shape: string

<a id="field-evaluated-at"></a>
## `evaluated/at`

- Required: `yes`
- Shape: string

<a id="field-valid-until"></a>
## `valid/until`

- Required: `yes`
- Shape: string

<a id="field-result"></a>
## `result`

- Required: `yes`
- Shape: const: `threshold-met`

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: string

<a id="field-release-not-after"></a>
## `release/not-after`

- Required: `yes`
- Shape: string

<a id="field-request-digest"></a>
## `request/digest`

- Required: `no`
- Shape: string
