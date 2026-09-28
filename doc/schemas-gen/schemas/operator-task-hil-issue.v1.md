# Operator Task HIL Issue v1

Source schema: [`doc/schemas/operator-task-hil-issue.v1.schema.json`](../../schemas/operator-task-hil-issue.v1.schema.json)

Request to issue, or find, the HIL requests of one stored plan for the binding it was compiled for. Each immutable request is persisted before delivery. Interrupted delivery retries that same request and deadline idempotently; a completed delivery receipt prevents repeated attention admission, including after defer or deny.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-hil-issue.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`plan/ref`](#field-plan-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-hil-issue.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-plan-ref"></a>
## `plan/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`
