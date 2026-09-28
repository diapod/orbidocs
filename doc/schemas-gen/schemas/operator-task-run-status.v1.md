# Operator Task Run Status v1

Source schema: [`doc/schemas/operator-task-run-status.v1.schema.json`](../../schemas/operator-task-run-status.v1.schema.json)

Projection of one run's append-only facts (P094-021f): where it stands, each started step's outcome, its conclusion and whether its instance is confirmed destroyed. It carries refs and tabled codes only, never command output.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-run-status.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`run/ref`](#field-run-ref) | `yes` | unspecified |  |
| [`binding/ref`](#field-binding-ref) | `yes` | unspecified |  |
| [`plan/ref`](#field-plan-ref) | `yes` | unspecified |  |
| [`phase`](#field-phase) | `yes` | enum: `running`, `rollback-pending`, `terminal` |  |
| [`environment/ref`](#field-environment-ref) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`steps`](#field-steps) | `yes` | array |  |
| [`cancel/requested`](#field-cancel-requested) | `yes` | boolean |  |
| [`conclusion`](#field-conclusion) | `no` | object |  |
| [`destruction/confirmation-ref`](#field-destruction-confirmation-ref) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "phase": {
      "const": "running"
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
          "conclusion"
        ]
      },
      {
        "required": [
          "destruction/confirmation-ref"
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
  "properties": {
    "phase": {
      "const": "rollback-pending"
    }
  }
}
```

Then:

```json
{
  "required": [
    "conclusion"
  ],
  "not": {
    "required": [
      "destruction/confirmation-ref"
    ]
  }
}
```

### Rule 3

When:

```json
{
  "properties": {
    "phase": {
      "const": "terminal"
    }
  }
}
```

Then:

```json
{
  "required": [
    "conclusion",
    "destruction/confirmation-ref"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-run-status.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-run-ref"></a>
## `run/ref`

- Required: `yes`
- Shape: unspecified

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: unspecified

<a id="field-plan-ref"></a>
## `plan/ref`

- Required: `yes`
- Shape: unspecified

<a id="field-phase"></a>
## `phase`

- Required: `yes`
- Shape: enum: `running`, `rollback-pending`, `terminal`

<a id="field-environment-ref"></a>
## `environment/ref`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-steps"></a>
## `steps`

- Required: `yes`
- Shape: array

<a id="field-cancel-requested"></a>
## `cancel/requested`

- Required: `yes`
- Shape: boolean

<a id="field-conclusion"></a>
## `conclusion`

- Required: `no`
- Shape: object

<a id="field-destruction-confirmation-ref"></a>
## `destruction/confirmation-ref`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`
