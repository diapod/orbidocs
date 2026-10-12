# Messaging-readiness.local.v1

Source schema: [`doc/schemas/messaging-readiness.local.v1.schema.json`](../../schemas/messaging-readiness.local.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/097-fresh-identity-onboarding-and-messaging-readiness.md`](../../project/40-proposals/097-fresh-identity-onboarding-and-messaging-readiness.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `messaging-readiness.local.v1` |  |
| [`subject`](#field-subject) | `yes` | object |  |
| [`requirements`](#field-requirements) | `yes` | const: `messaging-local-preparation@v1` |  |
| [`roles`](#field-roles) | `yes` | object |  |
| [`setup/status`](#field-setup-status) | `yes` | enum: `ready`, `blocked`, `unknown`, `not-requested` |  |
| [`observed_at`](#field-observed-at) | `yes` | string |  |
| [`federation_issuer_status`](#field-federation-issuer-status) | `yes` | enum: `ready`, `blocked`, `unknown`, `not-requested` |  |
| [`onboarding_deferred`](#field-onboarding-deferred) | `yes` | boolean |  |
| [`evidence`](#field-evidence) | `yes` | object |  |
| [`allowed_actions`](#field-allowed-actions) | `yes` | array |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `messaging-readiness.local.v1`

<a id="field-subject"></a>
## `subject`

- Required: `yes`
- Shape: object

<a id="field-requirements"></a>
## `requirements`

- Required: `yes`
- Shape: const: `messaging-local-preparation@v1`

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
