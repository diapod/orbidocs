# Agent External Runtime Turn Outcome v1

Source schema: [`doc/schemas/agent.external-runtime.turn-outcome.v1.schema.json`](../../schemas/agent.external-runtime.turn-outcome.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agent.external-runtime.turn-outcome.v1` |  |
| [`outcome/ref`](#field-outcome-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`turn/ref`](#field-turn-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`agent/id`](#field-agent-id) | `yes` | ref: `#/$defs/ref` |  |
| [`status`](#field-status) | `yes` | enum: `completed`, `refused`, `failed`, `cancelled`, `unknown` |  |
| [`reason/code`](#field-reason-code) | `yes` | ref: `#/$defs/reason-code` |  |
| [`retryability`](#field-retryability) | `yes` | enum: `terminal`, `retryable`, `reconciliation-required` |  |
| [`product/ref`](#field-product-ref) | `no` | ref: `#/$defs/ref` |  |
| [`product/digest`](#field-product-digest) | `no` | ref: `#/$defs/digest` |  |
| [`budget/reserved`](#field-budget-reserved) | `yes` | ref: `#/$defs/finite-budget` |  |
| [`budget/charged`](#field-budget-charged) | `yes` | ref: `#/$defs/usage-value` |  |
| [`usage/fidelity`](#field-usage-fidelity) | `yes` | enum: `authoritative`, `host-measured`, `estimated`, `unavailable` |  |
| [`session/checkpoint-ref`](#field-session-checkpoint-ref) | `no` | ref: `#/$defs/ref` |  |
| [`selected/at`](#field-selected-at) | `yes` | string |  |
| [`selected/by`](#field-selected-by) | `yes` | ref: `#/$defs/ref` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`positive-safe-integer`](#def-positive-safe-integer) | integer |  |
| [`finite-budget`](#def-finite-budget) | object |  |
| [`usage-value`](#def-usage-value) | object |  |
| [`reason-code`](#def-reason-code) | enum: `completed`, `policy-denied`, `binding-missing`, `binding-stale`, `binding-mismatch`, `binding-expired`, `binding-revoked`, `profile-disabled`, `profile-mismatch`, `budget-exhausted`, `usage-missing`, `usage-malformed`, `usage-overflow`, `usage-conflict`, `session-fence-mismatch`, `session-lost`, `event-malformed`, `event-duplicate`, `event-reordered`, `event-oversized`, `event-unauthorized`, `event-stale`, `event-timeout`, `tool-not-admitted`, `approval-not-admitted`, `provider-unavailable`, `cancelled`, `unknown` |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "status": {
      "const": "completed"
    }
  }
}
```

Then:

```json
{
  "required": [
    "product/ref",
    "product/digest"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "status": {
      "enum": [
        "refused",
        "failed",
        "cancelled",
        "unknown"
      ]
    }
  }
}
```

Then:

```json
{
  "not": {
    "anyOf": [
      {
        "required": [
          "product/ref"
        ]
      },
      {
        "required": [
          "product/digest"
        ]
      }
    ]
  }
}
```

### Rule 3

When:

```json
{
  "properties": {
    "status": {
      "const": "unknown"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "retryability": {
      "const": "reconciliation-required"
    },
    "reason/code": {
      "const": "unknown"
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.external-runtime.turn-outcome.v1`

<a id="field-outcome-ref"></a>
## `outcome/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-turn-ref"></a>
## `turn/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-agent-id"></a>
## `agent/id`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `completed`, `refused`, `failed`, `cancelled`, `unknown`

<a id="field-reason-code"></a>
## `reason/code`

- Required: `yes`
- Shape: ref: `#/$defs/reason-code`

<a id="field-retryability"></a>
## `retryability`

- Required: `yes`
- Shape: enum: `terminal`, `retryable`, `reconciliation-required`

<a id="field-product-ref"></a>
## `product/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-product-digest"></a>
## `product/digest`

- Required: `no`
- Shape: ref: `#/$defs/digest`

<a id="field-budget-reserved"></a>
## `budget/reserved`

- Required: `yes`
- Shape: ref: `#/$defs/finite-budget`

<a id="field-budget-charged"></a>
## `budget/charged`

- Required: `yes`
- Shape: ref: `#/$defs/usage-value`

<a id="field-usage-fidelity"></a>
## `usage/fidelity`

- Required: `yes`
- Shape: enum: `authoritative`, `host-measured`, `estimated`, `unavailable`

<a id="field-session-checkpoint-ref"></a>
## `session/checkpoint-ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-selected-at"></a>
## `selected/at`

- Required: `yes`
- Shape: string

<a id="field-selected-by"></a>
## `selected/by`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-positive-safe-integer"></a>
## `$defs.positive-safe-integer`

- Shape: integer

<a id="def-finite-budget"></a>
## `$defs.finite-budget`

- Shape: object

<a id="def-usage-value"></a>
## `$defs.usage-value`

- Shape: object

<a id="def-reason-code"></a>
## `$defs.reason-code`

- Shape: enum: `completed`, `policy-denied`, `binding-missing`, `binding-stale`, `binding-mismatch`, `binding-expired`, `binding-revoked`, `profile-disabled`, `profile-mismatch`, `budget-exhausted`, `usage-missing`, `usage-malformed`, `usage-overflow`, `usage-conflict`, `session-fence-mismatch`, `session-lost`, `event-malformed`, `event-duplicate`, `event-reordered`, `event-oversized`, `event-unauthorized`, `event-stale`, `event-timeout`, `tool-not-admitted`, `approval-not-admitted`, `provider-unavailable`, `cancelled`, `unknown`
