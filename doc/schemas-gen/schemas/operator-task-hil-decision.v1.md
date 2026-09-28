# Operator Task HIL Decision v1

Source schema: [`doc/schemas/operator-task-hil-decision.v1.schema.json`](../../schemas/operator-task-hil-decision.v1.schema.json)

The host's record of one answered HIL request: the request, plan and step it decides, the decision, and the verified operator binding and participant that made it. It is written once; a different answer to the same request refuses. Approval is bound to that plan step and is consumed by the step fence at use; it is never remembered for another plan or step.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-hil-decision.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`request/ref`](#field-request-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`plan/ref`](#field-plan-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`step/id`](#field-step-id) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/name` |  |
| [`decision`](#field-decision) | `yes` | enum: `approve`, `deny` |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/operatorBindingRef` |  |
| [`participant/ref`](#field-participant-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`decided-at`](#field-decided-at) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/timestamp` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-hil-decision.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-request-ref"></a>
## `request/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-plan-ref"></a>
## `plan/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-step-id"></a>
## `step/id`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/name`

<a id="field-decision"></a>
## `decision`

- Required: `yes`
- Shape: enum: `approve`, `deny`

<a id="field-operator-binding-ref"></a>
## `operator/binding-ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/operatorBindingRef`

<a id="field-participant-ref"></a>
## `participant/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-decided-at"></a>
## `decided-at`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/timestamp`
