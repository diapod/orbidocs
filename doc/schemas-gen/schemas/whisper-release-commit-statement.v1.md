# Whisper-release-commit-statement.v1

Source schema: [`doc/schemas/whisper-release-commit-statement.v1.schema.json`](../../schemas/whisper-release-commit-statement.v1.schema.json)

Public single-audience ADC commit statement under the fixed admitted case authority. No private Acceptance, source count, revisions or other audiences. Signature origin and exact consent binding are separate from actual owner commit/exposure and independent author admission.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-release-commit-statement.v1` |  |
| [`release/id`](#field-release-id) | `yes` | string |  |
| [`condition/original`](#field-condition-original) | `yes` | string |  |
| [`manifest/digest`](#field-manifest-digest) | `yes` | string |  |
| [`intent/digest`](#field-intent-digest) | `yes` | string |  |
| [`audience`](#field-audience) | `yes` | ref: `room-release-audience.v1.schema.json` |  |
| [`executor`](#field-executor) | `yes` | string |  |
| [`handover/by`](#field-handover-by) | `yes` | integer |  |
| [`condition`](#field-condition) | `yes` | object |  |
| [`case/authority`](#field-case-authority) | `yes` | string |  |
| [`attested/at`](#field-attested-at) | `yes` | string |  |
| [`result`](#field-result) | `yes` | const: `satisfied` |  |
| [`signature`](#field-signature) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-release-commit-statement.v1`

<a id="field-release-id"></a>
## `release/id`

- Required: `yes`
- Shape: string

<a id="field-condition-original"></a>
## `condition/original`

- Required: `yes`
- Shape: string

<a id="field-manifest-digest"></a>
## `manifest/digest`

- Required: `yes`
- Shape: string

<a id="field-intent-digest"></a>
## `intent/digest`

- Required: `yes`
- Shape: string

<a id="field-audience"></a>
## `audience`

- Required: `yes`
- Shape: ref: `room-release-audience.v1.schema.json`

<a id="field-executor"></a>
## `executor`

- Required: `yes`
- Shape: string

<a id="field-handover-by"></a>
## `handover/by`

- Required: `yes`
- Shape: integer

<a id="field-condition"></a>
## `condition`

- Required: `yes`
- Shape: object

<a id="field-case-authority"></a>
## `case/authority`

- Required: `yes`
- Shape: string

<a id="field-attested-at"></a>
## `attested/at`

- Required: `yes`
- Shape: string

<a id="field-result"></a>
## `result`

- Required: `yes`
- Shape: const: `satisfied`

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: string
