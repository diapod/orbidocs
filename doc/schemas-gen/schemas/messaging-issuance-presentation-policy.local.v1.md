# Messaging Issuance Presentation Policy

Source schema: [`doc/schemas/messaging-issuance-presentation-policy.local.v1.schema.json`](../../schemas/messaging-issuance-presentation-policy.local.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/076-limited-messaging-grants-decision.md`](../../project/40-proposals/076-limited-messaging-grants-decision.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`delegation_id`](#field-delegation-id) | `yes` | string |  |
| [`status_disclosure`](#field-status-disclosure) | `yes` | enum: `omit`, `full-status` |  |
## Field Semantics

<a id="field-delegation-id"></a>
## `delegation_id`

- Required: `yes`
- Shape: string

<a id="field-status-disclosure"></a>
## `status_disclosure`

- Required: `yes`
- Shape: enum: `omit`, `full-status`
