# Nym-renewal-readback.local.v1

Source schema: [`doc/schemas/nym-renewal-readback.local.v1.schema.json`](../../schemas/nym-renewal-readback.local.v1.schema.json)

Protected readback of sealed stay-ready consent. Execution remains separately guarded and is not enabled by this surface.

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `nym-renewal-readback.local.v1` |  |
| [`profile/digest`](#field-profile-digest) | `yes` | string |  |
| [`context/digest`](#field-context-digest) | `yes` | string |  |
| [`consent/ref`](#field-consent-ref) | `yes` | string |  |
| [`consent/id`](#field-consent-id) | `yes` | string |  |
| [`certification/id`](#field-certification-id) | `yes` | string |  |
| [`epoch`](#field-epoch) | `yes` | integer |  |
| [`revision`](#field-revision) | `yes` | integer |  |
| [`maximum/renewals`](#field-maximum-renewals) | `yes` | integer |  |
| [`reserved/renewals`](#field-reserved-renewals) | `yes` | integer |  |
| [`state`](#field-state) | `yes` | enum: `approved`, `revoked`, `epoch-ended` |  |
| [`approved/at`](#field-approved-at) | `yes` | string |  |
| [`consent/until`](#field-consent-until) | `yes` | string |  |
| [`revoked/at`](#field-revoked-at) | `yes` | unspecified |  |
| [`execution/state`](#field-execution-state) | `yes` | const: `not-enabled` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `nym-renewal-readback.local.v1`

<a id="field-profile-digest"></a>
## `profile/digest`

- Required: `yes`
- Shape: string

<a id="field-context-digest"></a>
## `context/digest`

- Required: `yes`
- Shape: string

<a id="field-consent-ref"></a>
## `consent/ref`

- Required: `yes`
- Shape: string

<a id="field-consent-id"></a>
## `consent/id`

- Required: `yes`
- Shape: string

<a id="field-certification-id"></a>
## `certification/id`

- Required: `yes`
- Shape: string

<a id="field-epoch"></a>
## `epoch`

- Required: `yes`
- Shape: integer

<a id="field-revision"></a>
## `revision`

- Required: `yes`
- Shape: integer

<a id="field-maximum-renewals"></a>
## `maximum/renewals`

- Required: `yes`
- Shape: integer

<a id="field-reserved-renewals"></a>
## `reserved/renewals`

- Required: `yes`
- Shape: integer

<a id="field-state"></a>
## `state`

- Required: `yes`
- Shape: enum: `approved`, `revoked`, `epoch-ended`

<a id="field-approved-at"></a>
## `approved/at`

- Required: `yes`
- Shape: string

<a id="field-consent-until"></a>
## `consent/until`

- Required: `yes`
- Shape: string

<a id="field-revoked-at"></a>
## `revoked/at`

- Required: `yes`
- Shape: unspecified

<a id="field-execution-state"></a>
## `execution/state`

- Required: `yes`
- Shape: const: `not-enabled`
