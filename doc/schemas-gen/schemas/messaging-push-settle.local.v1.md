# Local Messaging Admission Fact Settlement

Source schema: [`doc/schemas/messaging-push-settle.local.v1.schema.json`](../../schemas/messaging-push-settle.local.v1.schema.json)

## Governing Basis

- [`doc/project/60-solutions/027-messaging-middleware/027-messaging-middleware.md#consent-loss-recovery`](../../project/60-solutions/027-messaging-middleware/027-messaging-middleware.md#consent-loss-recovery)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `messaging-push-settle.local.v1` |  |
| [`operation`](#field-operation) | `yes` | enum: `record`, `acknowledge` |  |
| [`fact`](#field-fact) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `messaging-push-settle.local.v1`

<a id="field-operation"></a>
## `operation`

- Required: `yes`
- Shape: enum: `record`, `acknowledge`

<a id="field-fact"></a>
## `fact`

- Required: `yes`
- Shape: object
