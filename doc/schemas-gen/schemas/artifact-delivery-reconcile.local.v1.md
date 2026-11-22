# Exact Local Artifact Delivery Reconciliation Request

Source schema: [`doc/schemas/artifact-delivery-reconcile.local.v1.schema.json`](../../schemas/artifact-delivery-reconcile.local.v1.schema.json)

## Governing Basis

- [`doc/project/60-solutions/027-messaging-middleware/027-messaging-middleware.md#consent-loss-recovery`](../../project/60-solutions/027-messaging-middleware/027-messaging-middleware.md#consent-loss-recovery)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `artifact-delivery-reconcile.local.v1` |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | string |  |
| [`submission/digest`](#field-submission-digest) | `yes` | string |  |
| [`delivery/id`](#field-delivery-id) | `no` | string |  |
| [`timeout/ms`](#field-timeout-ms) | `yes` | integer |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `artifact-delivery-reconcile.local.v1`

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `yes`
- Shape: string

<a id="field-submission-digest"></a>
## `submission/digest`

- Required: `yes`
- Shape: string

<a id="field-delivery-id"></a>
## `delivery/id`

- Required: `no`
- Shape: string

<a id="field-timeout-ms"></a>
## `timeout/ms`

- Required: `yes`
- Shape: integer
