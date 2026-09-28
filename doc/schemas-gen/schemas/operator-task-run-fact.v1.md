# Operator Task Run Fact v1

Source schema: [`doc/schemas/operator-task-run-fact.v1.schema.json`](../../schemas/operator-task-run-fact.v1.schema.json)

One immutable transition of one task run. A run is the ordered sequence of its facts, numbered contiguously from 1 for `admitted`; its state and its `operator-task-experiment-result.v1` are projections, never a second stored record. The host records a fact before it acts on it: `step-started` is the durable admission point of a step's effect, so a step started without an outcome is `unknown` after a crash and is never repeated. `concluded` records how the run ended; the run is terminal only after `destruction-confirmed`, the environment owner's durable confirmation that the run's exclusive instance is gone.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-run-fact.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`run/ref`](#field-run-ref) | `yes` | unspecified |  |
| [`sequence`](#field-sequence) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/counter` |  |
| [`recorded-at`](#field-recorded-at) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/timestamp` |  |
| [`fact`](#field-fact) | `yes` | unspecified |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`stepOutcome`](#def-stepoutcome) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-run-fact.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-run-ref"></a>
## `run/ref`

- Required: `yes`
- Shape: unspecified

<a id="field-sequence"></a>
## `sequence`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/counter`

<a id="field-recorded-at"></a>
## `recorded-at`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/timestamp`

<a id="field-fact"></a>
## `fact`

- Required: `yes`
- Shape: unspecified

## Definition Semantics

<a id="def-stepoutcome"></a>
## `$defs.stepOutcome`

- Shape: object
