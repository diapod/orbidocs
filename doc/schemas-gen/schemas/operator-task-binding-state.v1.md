# Operator Task Binding State v1

Source schema: [`doc/schemas/operator-task-binding-state.v1.schema.json`](../../schemas/operator-task-binding-state.v1.schema.json)

Request to pause or resume one local binding. Pausing is reversible and needs no reactivation; revocation stays a P085 operation.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-binding-state.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`binding/state`](#field-binding-state) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/bindingState` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-binding-state.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-binding-state"></a>
## `binding/state`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/bindingState`
