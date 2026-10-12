# Capability-passport-preparation.local.v1

Source schema: [`doc/schemas/capability-passport-preparation.local.v1.schema.json`](../../schemas/capability-passport-preparation.local.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/097-fresh-identity-onboarding-and-messaging-readiness.md`](../../project/40-proposals/097-fresh-identity-onboarding-and-messaging-readiness.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`participant_id`](#field-participant-id) | `yes` | string |  |
| [`plan_revision`](#field-plan-revision) | `yes` | string |  |
| [`idempotency_key`](#field-idempotency-key) | `yes` | string |  |
| [`issue`](#field-issue) | `yes` | object |  |
## Field Semantics

<a id="field-participant-id"></a>
## `participant_id`

- Required: `yes`
- Shape: string

<a id="field-plan-revision"></a>
## `plan_revision`

- Required: `yes`
- Shape: string

<a id="field-idempotency-key"></a>
## `idempotency_key`

- Required: `yes`
- Shape: string

<a id="field-issue"></a>
## `issue`

- Required: `yes`
- Shape: object
