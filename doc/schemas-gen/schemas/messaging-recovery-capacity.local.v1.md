# Current Node-local Messaging Recovery Capacity

Source schema: [`doc/schemas/messaging-recovery-capacity.local.v1.schema.json`](../../schemas/messaging-recovery-capacity.local.v1.schema.json)

## Governing Basis

- [`doc/project/60-solutions/027-messaging-middleware/027-messaging-middleware.md`](../../project/60-solutions/027-messaging-middleware/027-messaging-middleware.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `messaging-recovery-capacity.local.v1` |  |
| [`resolution/id`](#field-resolution-id) | `yes` | string |  |
| [`policy`](#field-policy) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `messaging-recovery-capacity.local.v1`

<a id="field-resolution-id"></a>
## `resolution/id`

- Required: `yes`
- Shape: string

<a id="field-policy"></a>
## `policy`

- Required: `yes`
- Shape: object
