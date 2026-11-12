# Weak-signal-custody-extend.local.v1

Source schema: [`doc/schemas/weak-signal-custody-extend.local.v1.schema.json`](../../schemas/weak-signal-custody-extend.local.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`finding/id`](#field-finding-id) | `yes` | string |  |
| [`expected/claims`](#field-expected-claims) | `yes` | array |  |
| [`retention/seconds`](#field-retention-seconds) | `yes` | integer |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | string |  |
## Field Semantics

<a id="field-finding-id"></a>
## `finding/id`

- Required: `yes`
- Shape: string

<a id="field-expected-claims"></a>
## `expected/claims`

- Required: `yes`
- Shape: array

<a id="field-retention-seconds"></a>
## `retention/seconds`

- Required: `yes`
- Shape: integer

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `yes`
- Shape: string
