# Messaging-readiness.local.v2

Source schema: [`doc/schemas/messaging-readiness.local.v2.schema.json`](../../schemas/messaging-readiness.local.v2.schema.json)

## Governing Basis

- [`doc/project/40-proposals/097-fresh-identity-onboarding-and-messaging-readiness.md`](../../project/40-proposals/097-fresh-identity-onboarding-and-messaging-readiness.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `messaging-readiness.local.v2` |  |
| [`subject`](#field-subject) | `yes` | object |  |
| [`requirements`](#field-requirements) | `yes` | const: `messaging-local-preparation@v2` |  |
| [`roles`](#field-roles) | `yes` | object |  |
| [`setup/status`](#field-setup-status) | `yes` | enum: `ready`, `blocked`, `unknown`, `not-requested` |  |
| [`observed_at`](#field-observed-at) | `yes` | string |  |
| [`issuance/status-refresh`](#field-issuance-status-refresh) | `no` | object |  |
| [`federation_issuer_status`](#field-federation-issuer-status) | `yes` | enum: `ready`, `blocked`, `unknown`, `not-requested` |  |
| [`onboarding_deferred`](#field-onboarding-deferred) | `yes` | boolean |  |
| [`evidence`](#field-evidence) | `yes` | object |  |
| [`allowed_actions`](#field-allowed-actions) | `yes` | array |  |
| [`issuance_authority_status`](#field-issuance-authority-status) | `yes` | enum: `ready`, `blocked`, `unknown`, `not-requested` |  |
| [`issuance_authority_kind`](#field-issuance-authority-kind) | `yes` | enum: `sovereign`, `delegated`, `none` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `messaging-readiness.local.v2`

<a id="field-subject"></a>
## `subject`

- Required: `yes`
- Shape: object

<a id="field-requirements"></a>
## `requirements`

- Required: `yes`
- Shape: const: `messaging-local-preparation@v2`

<a id="field-roles"></a>
## `roles`

- Required: `yes`
- Shape: object

<a id="field-setup-status"></a>
## `setup/status`

- Required: `yes`
- Shape: enum: `ready`, `blocked`, `unknown`, `not-requested`

<a id="field-observed-at"></a>
## `observed_at`

- Required: `yes`
- Shape: string

<a id="field-issuance-status-refresh"></a>
## `issuance/status-refresh`

- Required: `no`
- Shape: object

<a id="field-federation-issuer-status"></a>
## `federation_issuer_status`

- Required: `yes`
- Shape: enum: `ready`, `blocked`, `unknown`, `not-requested`

<a id="field-onboarding-deferred"></a>
## `onboarding_deferred`

- Required: `yes`
- Shape: boolean

<a id="field-evidence"></a>
## `evidence`

- Required: `yes`
- Shape: object

<a id="field-allowed-actions"></a>
## `allowed_actions`

- Required: `yes`
- Shape: array

<a id="field-issuance-authority-status"></a>
## `issuance_authority_status`

- Required: `yes`
- Shape: enum: `ready`, `blocked`, `unknown`, `not-requested`

<a id="field-issuance-authority-kind"></a>
## `issuance_authority_kind`

- Required: `yes`
- Shape: enum: `sovereign`, `delegated`, `none`
