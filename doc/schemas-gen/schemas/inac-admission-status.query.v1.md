# INAC Exact-attempt Admission Query

Source schema: [`doc/schemas/inac-admission-status.query.v1.schema.json`](../../schemas/inac-admission-status.query.v1.schema.json)

## Governing Basis

- [`doc/project/60-solutions/027-messaging-middleware/027-messaging-middleware.md#consent-loss-recovery`](../../project/60-solutions/027-messaging-middleware/027-messaging-middleware.md#consent-loss-recovery)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `inac-admission-status.query.v1` |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | string |  |
| [`artifact/id`](#field-artifact-id) | `yes` | string |  |
| [`artifact/digest`](#field-artifact-digest) | `yes` | string |  |
| [`message/commitment`](#field-message-commitment) | `yes` | string |  |
| [`resume/until`](#field-resume-until) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `inac-admission-status.query.v1`

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `yes`
- Shape: string

<a id="field-artifact-id"></a>
## `artifact/id`

- Required: `yes`
- Shape: string

<a id="field-artifact-digest"></a>
## `artifact/digest`

- Required: `yes`
- Shape: string

<a id="field-message-commitment"></a>
## `message/commitment`

- Required: `yes`
- Shape: string

<a id="field-resume-until"></a>
## `resume/until`

- Required: `yes`
- Shape: string
