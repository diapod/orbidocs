# Operator Task Experiment Result v1

Source schema: [`doc/schemas/operator-task-experiment-result.v1.schema.json`](../../schemas/operator-task-experiment-result.v1.schema.json)

Links to owner-domain evidence of one task run. Prompts, secrets, raw VM files, private command output, and chain-of-thought are never carried.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-experiment-result.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`run/ref`](#field-run-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`plan/ref`](#field-plan-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`plan/digest`](#field-plan-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`task-profile/digest`](#field-task-profile-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`local-binding/digest`](#field-local-binding-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`activation/generation`](#field-activation-generation) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/counter` |  |
| [`outcome`](#field-outcome) | `yes` | enum: `verified`, `verification-failed`, `refused`, `cancelled`, `unknown` |  |
| [`refusal/code`](#field-refusal-code) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/refusalCode` |  |
| [`deliberation`](#field-deliberation) | `no` | object |  |
| [`steps`](#field-steps) | `yes` | array |  |
| [`verifier`](#field-verifier) | `no` | object |  |
| [`rollback`](#field-rollback) | `yes` | object |  |
| [`timings`](#field-timings) | `yes` | object |  |
| [`resource-accounting/ref`](#field-resource-accounting-ref) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`disclosure`](#field-disclosure) | `yes` | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "outcome": {
      "const": "refused"
    }
  }
}
```

Then:

```json
{
  "required": [
    "refusal/code"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "outcome": {
      "enum": [
        "verified",
        "verification-failed"
      ]
    }
  }
}
```

Then:

```json
{
  "required": [
    "verifier"
  ]
}
```

### Rule 3

When:

```json
{
  "properties": {
    "outcome": {
      "const": "verified"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "verifier": {
      "properties": {
        "passed": {
          "const": true
        }
      }
    }
  }
}
```

### Rule 4

When:

```json
{
  "properties": {
    "outcome": {
      "const": "verification-failed"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "verifier": {
      "properties": {
        "passed": {
          "const": false
        }
      }
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-experiment-result.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-run-ref"></a>
## `run/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-plan-ref"></a>
## `plan/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-plan-digest"></a>
## `plan/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-task-profile-digest"></a>
## `task-profile/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-local-binding-digest"></a>
## `local-binding/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-activation-generation"></a>
## `activation/generation`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/counter`

<a id="field-outcome"></a>
## `outcome`

- Required: `yes`
- Shape: enum: `verified`, `verification-failed`, `refused`, `cancelled`, `unknown`

<a id="field-refusal-code"></a>
## `refusal/code`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/refusalCode`

<a id="field-deliberation"></a>
## `deliberation`

- Required: `no`
- Shape: object

<a id="field-steps"></a>
## `steps`

- Required: `yes`
- Shape: array

<a id="field-verifier"></a>
## `verifier`

- Required: `no`
- Shape: object

<a id="field-rollback"></a>
## `rollback`

- Required: `yes`
- Shape: object

<a id="field-timings"></a>
## `timings`

- Required: `yes`
- Shape: object

<a id="field-resource-accounting-ref"></a>
## `resource-accounting/ref`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-disclosure"></a>
## `disclosure`

- Required: `yes`
- Shape: object
