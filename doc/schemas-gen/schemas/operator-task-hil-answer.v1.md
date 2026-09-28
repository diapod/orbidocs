# Operator Task HIL Answer v1

Source schema: [`doc/schemas/operator-task-hil-answer.v1.schema.json`](../../schemas/operator-task-hil-answer.v1.schema.json)

An operator's answer to one HIL request, made under a current operator binding that the host verifies when it records the decision. It names the request only; the host takes the plan, step and decision material from its stored request, so an answer cannot approve anything else. `approve` authorizes that one step of that one plan once; `deny` refuses it. A request is answered at most once.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-hil-answer.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`request/ref`](#field-request-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/operatorBindingRef` |  |
| [`decision`](#field-decision) | `yes` | enum: `approve`, `deny` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-hil-answer.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-request-ref"></a>
## `request/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-operator-binding-ref"></a>
## `operator/binding-ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/operatorBindingRef`

<a id="field-decision"></a>
## `decision`

- Required: `yes`
- Shape: enum: `approve`, `deny`
