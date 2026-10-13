# Messaging Outbox Provenance Lifecycle Reconciliation v1

Source schema: [`doc/schemas/messaging-send-provenance-sync.local.v1.schema.json`](../../schemas/messaging-send-provenance-sync.local.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/097-fresh-identity-onboarding-and-messaging-readiness.md`](../../project/40-proposals/097-fresh-identity-onboarding-and-messaging-readiness.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`sweep`](#field-sweep) | `yes` | boolean |  |
| [`entries`](#field-entries) | `yes` | array |  |
## Field Semantics

<a id="field-sweep"></a>
## `sweep`

- Required: `yes`
- Shape: boolean

<a id="field-entries"></a>
## `entries`

- Required: `yes`
- Shape: array
