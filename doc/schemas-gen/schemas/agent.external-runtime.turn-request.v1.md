# Agent External Runtime Turn Request v1

Source schema: [`doc/schemas/agent.external-runtime.turn-request.v1.schema.json`](../../schemas/agent.external-runtime.turn-request.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agent.external-runtime.turn-request.v1` |  |
| [`turn/ref`](#field-turn-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`mode`](#field-mode) | `yes` | enum: `start`, `continue` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`binding/digest`](#field-binding-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`agent/id`](#field-agent-id) | `yes` | ref: `#/$defs/ref` |  |
| [`passage/ref`](#field-passage-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`passage/no`](#field-passage-no) | `yes` | integer |  |
| [`kind`](#field-kind) | `yes` | enum: `draft`, `critique`, `revision`, `final` |  |
| [`parent-product/refs`](#field-parent-product-refs) | `yes` | array |  |
| [`input/parts`](#field-input-parts) | `yes` | array |  |
| [`input/digest`](#field-input-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`instruction/hash`](#field-instruction-hash) | `yes` | ref: `#/$defs/digest` |  |
| [`prompt-policy/ref`](#field-prompt-policy-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`output-schema/ref`](#field-output-schema-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`visibility`](#field-visibility) | `yes` | enum: `private`, `operator`, `shared` |  |
| [`classification`](#field-classification) | `yes` | ref: `classification.v1.schema.json` |  |
| [`budget/reservation`](#field-budget-reservation) | `yes` | ref: `#/$defs/finite-budget` |  |
| [`observation`](#field-observation) | `no` | ref: `#/$defs/observation` |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | ref: `#/$defs/ref` |  |
| [`deadline/at`](#field-deadline-at) | `yes` | string |  |
| [`admitted/at`](#field-admitted-at) | `yes` | string |  |
| [`admitted/by`](#field-admitted-by) | `yes` | ref: `#/$defs/ref` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`positive-safe-integer`](#def-positive-safe-integer) | integer |  |
| [`finite-budget`](#def-finite-budget) | object |  |
| [`input-part`](#def-input-part) | unspecified |  |
| [`observation`](#def-observation) | object |  |
| [`reason-code`](#def-reason-code) | enum: `completed`, `policy-denied`, `binding-missing`, `binding-stale`, `binding-mismatch`, `binding-expired`, `binding-revoked`, `profile-disabled`, `profile-mismatch`, `budget-exhausted`, `usage-missing`, `usage-malformed`, `usage-overflow`, `usage-conflict`, `session-fence-mismatch`, `session-lost`, `event-malformed`, `event-duplicate`, `event-reordered`, `event-oversized`, `event-unauthorized`, `event-stale`, `event-timeout`, `tool-not-admitted`, `approval-not-admitted`, `provider-unavailable`, `cancelled`, `unknown` |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "mode": {
      "const": "start"
    }
  }
}
```

Then:

```json
{
  "not": {
    "required": [
      "observation"
    ]
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "mode": {
      "const": "continue"
    }
  }
}
```

Then:

```json
{
  "required": [
    "observation"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.external-runtime.turn-request.v1`

<a id="field-turn-ref"></a>
## `turn/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-mode"></a>
## `mode`

- Required: `yes`
- Shape: enum: `start`, `continue`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-binding-digest"></a>
## `binding/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-agent-id"></a>
## `agent/id`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-passage-ref"></a>
## `passage/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-passage-no"></a>
## `passage/no`

- Required: `yes`
- Shape: integer

<a id="field-kind"></a>
## `kind`

- Required: `yes`
- Shape: enum: `draft`, `critique`, `revision`, `final`

<a id="field-parent-product-refs"></a>
## `parent-product/refs`

- Required: `yes`
- Shape: array

<a id="field-input-parts"></a>
## `input/parts`

- Required: `yes`
- Shape: array

<a id="field-input-digest"></a>
## `input/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-instruction-hash"></a>
## `instruction/hash`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-prompt-policy-ref"></a>
## `prompt-policy/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-output-schema-ref"></a>
## `output-schema/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-visibility"></a>
## `visibility`

- Required: `yes`
- Shape: enum: `private`, `operator`, `shared`

<a id="field-classification"></a>
## `classification`

- Required: `yes`
- Shape: ref: `classification.v1.schema.json`

<a id="field-budget-reservation"></a>
## `budget/reservation`

- Required: `yes`
- Shape: ref: `#/$defs/finite-budget`

<a id="field-observation"></a>
## `observation`

- Required: `no`
- Shape: ref: `#/$defs/observation`

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-deadline-at"></a>
## `deadline/at`

- Required: `yes`
- Shape: string

<a id="field-admitted-at"></a>
## `admitted/at`

- Required: `yes`
- Shape: string

<a id="field-admitted-by"></a>
## `admitted/by`

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

<a id="def-input-part"></a>
## `$defs.input-part`

- Shape: unspecified

<a id="def-observation"></a>
## `$defs.observation`

- Shape: object

<a id="def-reason-code"></a>
## `$defs.reason-code`

- Shape: enum: `completed`, `policy-denied`, `binding-missing`, `binding-stale`, `binding-mismatch`, `binding-expired`, `binding-revoked`, `profile-disabled`, `profile-mismatch`, `budget-exhausted`, `usage-missing`, `usage-malformed`, `usage-overflow`, `usage-conflict`, `session-fence-mismatch`, `session-lost`, `event-malformed`, `event-duplicate`, `event-reordered`, `event-oversized`, `event-unauthorized`, `event-stale`, `event-timeout`, `tool-not-admitted`, `approval-not-admitted`, `provider-unavailable`, `cancelled`, `unknown`
