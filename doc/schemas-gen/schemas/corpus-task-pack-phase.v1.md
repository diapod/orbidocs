# Corpus Task Pack Phase v1

Source schema: [`doc/schemas/corpus-task-pack-phase.v1.schema.json`](../../schemas/corpus-task-pack-phase.v1.schema.json)

Host fact derived from the latest signed execution of the logical round and its exact plan, result, admitted verifier evaluation and same-instance observations. Every basis is a required included manifest item. No execution means initial-observation; exact failed verification and all required successful untruncated nonempty observations mean repair-eligible; otherwise evidence-missing. Not model prose, a verdict or an effect grant. Exact Verified execution with a linked successful verifier yields goal-completed, never a missing failed-verification gap; further candidates refuse.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-phase.v1` |  |
| [`phase`](#field-phase) | `yes` | enum: `initial-observation`, `repair-eligible`, `evidence-missing`, `goal-completed` |  |
| [`rule/ref`](#field-rule-ref) | `yes` | string |  |
| [`rule/digest`](#field-rule-digest) | `yes` | string |  |
| [`basis`](#field-basis) | `yes` | array |  |
| [`missing`](#field-missing) | `yes` | array |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "phase": {
      "const": "initial-observation"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "basis": {
      "maxItems": 0
    },
    "missing": {
      "maxItems": 0
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "phase": {
      "const": "repair-eligible"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "basis": {
      "minItems": 3
    },
    "missing": {
      "maxItems": 0
    }
  }
}
```

### Rule 3

When:

```json
{
  "properties": {
    "phase": {
      "const": "evidence-missing"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "missing": {
      "minItems": 1
    }
  }
}
```

### Rule 4

When:

```json
{
  "properties": {
    "phase": {
      "const": "goal-completed"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "basis": {
      "minItems": 2
    },
    "missing": {
      "maxItems": 0
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-phase.v1`

<a id="field-phase"></a>
## `phase`

- Required: `yes`
- Shape: enum: `initial-observation`, `repair-eligible`, `evidence-missing`, `goal-completed`

<a id="field-rule-ref"></a>
## `rule/ref`

- Required: `yes`
- Shape: string

<a id="field-rule-digest"></a>
## `rule/digest`

- Required: `yes`
- Shape: string

<a id="field-basis"></a>
## `basis`

- Required: `yes`
- Shape: array

<a id="field-missing"></a>
## `missing`

- Required: `yes`
- Shape: array
