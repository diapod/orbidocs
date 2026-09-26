# Operator Task Experiment Plan v1

Source schema: [`doc/schemas/operator-task-experiment-plan.v1.schema.json`](../../schemas/operator-task-experiment-plan.v1.schema.json)

Host-validated plan derived from one candidate. Every step carries its exact profile digest and the host-derived capability, effect class and source, and HIL requirement.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-experiment-plan.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`plan/ref`](#field-plan-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`candidate/digest`](#field-candidate-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`task-profile/digest`](#field-task-profile-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`local-binding/digest`](#field-local-binding-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`activation/generation`](#field-activation-generation) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/counter` |  |
| [`steps`](#field-steps) | `yes` | array |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-experiment-plan.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-plan-ref"></a>
## `plan/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-candidate-digest"></a>
## `candidate/digest`

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

<a id="field-steps"></a>
## `steps`

- Required: `yes`
- Shape: array
