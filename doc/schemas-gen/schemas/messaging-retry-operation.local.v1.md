# Messaging Retry Operation

Source schema: [`doc/schemas/messaging-retry-operation.local.v1.schema.json`](../../schemas/messaging-retry-operation.local.v1.schema.json)

Durable owner-scoped retry receipts. Only initial preview creation returns the one-time confirmation token.

## Governing Basis

- [`doc/project/60-solutions/027-messaging-middleware/027-messaging-middleware.md#explicit-retry-operation`](../../project/60-solutions/027-messaging-middleware/027-messaging-middleware.md#explicit-retry-operation)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `messaging-retry-operation.local.v1` |  |
| [`operation`](#field-operation) | `yes` | ref: `#/$defs/operation` |  |
| [`confirmation/token`](#field-confirmation-token) | `no` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`operation-item`](#def-operation-item) | object |  |
| [`operation`](#def-operation) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `messaging-retry-operation.local.v1`

<a id="field-operation"></a>
## `operation`

- Required: `yes`
- Shape: ref: `#/$defs/operation`

<a id="field-confirmation-token"></a>
## `confirmation/token`

- Required: `no`
- Shape: string

## Definition Semantics

<a id="def-operation-item"></a>
## `$defs.operation-item`

- Shape: object

<a id="def-operation"></a>
## `$defs.operation`

- Shape: object
