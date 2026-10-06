# Operator Task Binding Maintenance Response v1

Source schema: [`doc/schemas/operator-task-binding-maintenance.response.v1.schema.json`](../../schemas/operator-task-binding-maintenance.response.v1.schema.json)

A bounded source maintenance observation. Preview is read-only. Recorded outcomes precede consumption, but never renew a package activation, operator binding, lease or run grant. Conflict never authorizes replacement.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-binding-maintenance.response.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`action`](#field-action) | `yes` | enum: `preview-migration`, `adopt-migration`, `recover` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`authority/renewed`](#field-authority-renewed) | `yes` | const: `False` |  |
| [`disposition`](#field-disposition) | `yes` | enum: `preview`, `recorded`, `no-intent` |  |
| [`plan`](#field-plan) | `no` | ref: `config-change-plan.v1.schema.json` |  |
| [`commit/outcome`](#field-commit-outcome) | `no` | enum: `None`, `committed`, `not-committed`, `recovered-committed`, `no-op-content`, `conflict` |  |
| [`transaction/ref`](#field-transaction-ref) | `no` | unspecified |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "required": [
    "action"
  ],
  "properties": {
    "action": {
      "const": "preview-migration"
    }
  }
}
```

Then:

```json
{
  "required": [
    "plan"
  ],
  "properties": {
    "disposition": {
      "const": "preview"
    }
  },
  "not": {
    "anyOf": [
      {
        "required": [
          "commit/outcome"
        ]
      },
      {
        "required": [
          "transaction/ref"
        ]
      }
    ]
  }
}
```

### Rule 2

When:

```json
{
  "required": [
    "disposition"
  ],
  "properties": {
    "disposition": {
      "const": "recorded"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "commit/outcome": {
      "type": "string"
    },
    "transaction/ref": {
      "type": "string"
    }
  }
}
```

### Rule 3

When:

```json
{
  "required": [
    "disposition"
  ],
  "properties": {
    "disposition": {
      "const": "no-intent"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "action": {
      "const": "recover"
    },
    "commit/outcome": {
      "type": "null"
    },
    "transaction/ref": {
      "type": "null"
    }
  }
}
```

### Rule 4

When:

```json
{
  "required": [
    "action"
  ],
  "properties": {
    "action": {
      "const": "adopt-migration"
    }
  }
}
```

Then:

```json
{
  "required": [
    "plan"
  ],
  "properties": {
    "disposition": {
      "const": "recorded"
    },
    "commit/outcome": {
      "const": "no-op-content"
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-binding-maintenance.response.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-action"></a>
## `action`

- Required: `yes`
- Shape: enum: `preview-migration`, `adopt-migration`, `recover`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-authority-renewed"></a>
## `authority/renewed`

- Required: `yes`
- Shape: const: `False`

<a id="field-disposition"></a>
## `disposition`

- Required: `yes`
- Shape: enum: `preview`, `recorded`, `no-intent`

<a id="field-plan"></a>
## `plan`

- Required: `no`
- Shape: ref: `config-change-plan.v1.schema.json`

<a id="field-commit-outcome"></a>
## `commit/outcome`

- Required: `no`
- Shape: enum: `None`, `committed`, `not-committed`, `recovered-committed`, `no-op-content`, `conflict`

<a id="field-transaction-ref"></a>
## `transaction/ref`

- Required: `no`
- Shape: unspecified
