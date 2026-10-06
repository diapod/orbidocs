# Operator Task Binding Maintenance Request v1

Source schema: [`doc/schemas/operator-task-binding-maintenance.request.v1.schema.json`](../../schemas/operator-task-binding-maintenance.request.v1.schema.json)

Explicit source migration or content recovery under current local operator authority. Adoption approves the complete previewed P091 plan; recovery observes bytes, never overwrites them or renews execution authority.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-binding-maintenance.request.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`action`](#field-action) | `yes` | enum: `preview-migration`, `adopt-migration`, `recover` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`plan`](#field-plan) | `no` | ref: `config-change-plan.v1.schema.json` |  |

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
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-binding-maintenance.request.v1`

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

<a id="field-operator-binding-ref"></a>
## `operator/binding-ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-plan"></a>
## `plan`

- Required: `no`
- Shape: ref: `config-change-plan.v1.schema.json`
