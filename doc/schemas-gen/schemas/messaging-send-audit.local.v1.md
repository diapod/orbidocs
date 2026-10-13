# Read-only Messaging Send Inventory v1

Source schema: [`doc/schemas/messaging-send-audit.local.v1.schema.json`](../../schemas/messaging-send-audit.local.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/097-fresh-identity-onboarding-and-messaging-readiness.md`](../../project/40-proposals/097-fresh-identity-onboarding-and-messaging-readiness.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `messaging-send-audit.local.v1` |  |
| [`profiles`](#field-profiles) | `yes` | array |  |
| [`next_cursor`](#field-next-cursor) | `yes` | string \| null |  |
| [`items`](#field-items) | `yes` | array |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `messaging-send-audit.local.v1`

<a id="field-profiles"></a>
## `profiles`

- Required: `yes`
- Shape: array

<a id="field-next-cursor"></a>
## `next_cursor`

- Required: `yes`
- Shape: string | null

<a id="field-items"></a>
## `items`

- Required: `yes`
- Shape: array
