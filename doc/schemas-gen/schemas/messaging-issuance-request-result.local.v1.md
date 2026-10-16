# Messaging-issuance-request-result.local.v1

Source schema: [`doc/schemas/messaging-issuance-request-result.local.v1.schema.json`](../../schemas/messaging-issuance-request-result.local.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/076-limited-messaging-grants-decision.md`](../../project/40-proposals/076-limited-messaging-grants-decision.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`request`](#field-request) | `yes` | ref: `capability-issuance-request.v1.schema.json` |  |
| [`key_id`](#field-key-id) | `yes` | string |  |
## Field Semantics

<a id="field-request"></a>
## `request`

- Required: `yes`
- Shape: ref: `capability-issuance-request.v1.schema.json`

<a id="field-key-id"></a>
## `key_id`

- Required: `yes`
- Shape: string
