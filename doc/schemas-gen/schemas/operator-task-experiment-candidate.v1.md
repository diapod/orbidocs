# Operator Task Experiment Candidate v1

Source schema: [`doc/schemas/operator-task-experiment-candidate.v1.schema.json`](../../schemas/operator-task-experiment-candidate.v1.schema.json)

Untrusted Agent or model output. Steps name closed action kinds and refs only; digests, capabilities, effect classes, HIL flags, binding identity, and activation generation are not representable.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-experiment-candidate.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`steps`](#field-steps) | `yes` | array |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-experiment-candidate.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-steps"></a>
## `steps`

- Required: `yes`
- Shape: array
