# Exact INAC Reservation Check for the Local Messaging Acceptor

Source schema: [`doc/schemas/messaging-push-check.local.v1.schema.json`](../../schemas/messaging-push-check.local.v1.schema.json)

## Governing Basis

- [`doc/project/60-solutions/027-messaging-middleware/027-messaging-middleware.md#consent-loss-recovery`](../../project/60-solutions/027-messaging-middleware/027-messaging-middleware.md#consent-loss-recovery)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `messaging-push-check.local.v1` |  |
| [`peer/node-id`](#field-peer-node-id) | `yes` | string |  |
| [`push`](#field-push) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `messaging-push-check.local.v1`

<a id="field-peer-node-id"></a>
## `peer/node-id`

- Required: `yes`
- Shape: string

<a id="field-push"></a>
## `push`

- Required: `yes`
- Shape: object
