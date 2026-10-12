# Issuer-admission-request-create.local.v1

Source schema: [`doc/schemas/issuer-admission-request-create.local.v1.schema.json`](../../schemas/issuer-admission-request-create.local.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/097-fresh-identity-onboarding-and-messaging-readiness.md`](../../project/40-proposals/097-fresh-identity-onboarding-and-messaging-readiness.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`participant_id`](#field-participant-id) | `yes` | string |  |
| [`requested_role`](#field-requested-role) | `yes` | const: `sovereign-passport-issuer` |  |
## Field Semantics

<a id="field-participant-id"></a>
## `participant_id`

- Required: `yes`
- Shape: string

<a id="field-requested-role"></a>
## `requested_role`

- Required: `yes`
- Shape: const: `sovereign-passport-issuer`
