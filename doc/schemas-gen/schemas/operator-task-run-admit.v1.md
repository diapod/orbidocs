# Operator Task Run Admit v1

Source schema: [`doc/schemas/operator-task-run-admit.v1.schema.json`](../../schemas/operator-task-run-admit.v1.schema.json)

Request to admit one run of a stored plan for the binding it was compiled for (P094-021f). The run ref is the content address of the plan ref and the run key, so admitting the same key again answers the admitted run. The background worker drives the run; this request never runs a step.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-run-admit.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | unspecified |  |
| [`plan/ref`](#field-plan-ref) | `yes` | unspecified |  |
| [`run/key`](#field-run-key) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-run-admit.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: unspecified

<a id="field-plan-ref"></a>
## `plan/ref`

- Required: `yes`
- Shape: unspecified

<a id="field-run-key"></a>
## `run/key`

- Required: `yes`
- Shape: string
