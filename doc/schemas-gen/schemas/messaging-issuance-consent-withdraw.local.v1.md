# Messaging-issuance-consent-withdraw.local.v1

Source schema: [`doc/schemas/messaging-issuance-consent-withdraw.local.v1.schema.json`](../../schemas/messaging-issuance-consent-withdraw.local.v1.schema.json)

Explicit local withdrawal of one child passport issued under a bounded grant. The bound node signs a capability-passport-revocation.v2 that targets the child; withdrawal of the parent grant uses messaging-issuance-withdraw.local.v1.

## Governing Basis

- [`doc/project/40-proposals/076-limited-messaging-grants-decision.md`](../../project/40-proposals/076-limited-messaging-grants-decision.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`passport_id`](#field-passport-id) | `yes` | string |  |
## Field Semantics

<a id="field-passport-id"></a>
## `passport_id`

- Required: `yes`
- Shape: string
