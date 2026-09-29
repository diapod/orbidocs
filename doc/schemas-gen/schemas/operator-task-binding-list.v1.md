# Operator Task Binding List v1

Source schema: [`doc/schemas/operator-task-binding-list.v1.schema.json`](../../schemas/operator-task-binding-list.v1.schema.json)

The operator's first view of local task-pack bindings (P094-012): one row per binding in ref order with its state, whether it is runnable, and its decisive readiness blocker with the next action. Rows carry refs only; the drill-down is operator-task-binding-inspection.v1.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-binding-list.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`evaluated-at`](#field-evaluated-at) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/timestamp` |  |
| [`bindings`](#field-bindings) | `yes` | array |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-binding-list.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-evaluated-at"></a>
## `evaluated-at`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/timestamp`

<a id="field-bindings"></a>
## `bindings`

- Required: `yes`
- Shape: array
