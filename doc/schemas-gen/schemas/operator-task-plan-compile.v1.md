# Operator Task Plan Compile v1

Source schema: [`doc/schemas/operator-task-plan-compile.v1.schema.json`](../../schemas/operator-task-plan-compile.v1.schema.json)

Request to compile one untrusted experiment candidate into the immutable plan of one local binding. The host admits the candidate under the checked-in candidate contract and the candidate schema the profile pins, requires the binding to be ready for a run, stamps every derived fact, and admits every patch file before storing the plan create-only. Compiling the same candidate for the same binding revision again returns the stored plan.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-plan-compile.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`candidate`](#field-candidate) | `yes` | ref: `operator-task-experiment-candidate.v1.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-plan-compile.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-candidate"></a>
## `candidate`

- Required: `yes`
- Shape: ref: `operator-task-experiment-candidate.v1.schema.json`
