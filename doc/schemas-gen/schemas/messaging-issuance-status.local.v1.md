# Messaging-issuance-status.local.v1

Source schema: [`doc/schemas/messaging-issuance-status.local.v1.schema.json`](../../schemas/messaging-issuance-status.local.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/076-limited-messaging-grants-decision.md`](../../project/40-proposals/076-limited-messaging-grants-decision.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `messaging-issuance-status.local.v1` |  |
| [`participant_id`](#field-participant-id) | `yes` | string |  |
| [`observed_at`](#field-observed-at) | `yes` | string |  |
| [`grants`](#field-grants) | `yes` | array |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `messaging-issuance-status.local.v1`

<a id="field-participant-id"></a>
## `participant_id`

- Required: `yes`
- Shape: string

<a id="field-observed-at"></a>
## `observed_at`

- Required: `yes`
- Shape: string

<a id="field-grants"></a>
## `grants`

- Required: `yes`
- Shape: array
