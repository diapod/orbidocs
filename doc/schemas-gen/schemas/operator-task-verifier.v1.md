# Operator Task Verifier v1

Source schema: [`doc/schemas/operator-task-verifier.v1.schema.json`](../../schemas/operator-task-verifier.v1.schema.json)

A task pack's verifier: the named checks its result must report, every one of them, the time the verifier may take, and how often a timed-out verifier may run again. The verifier runs as an enforced observation after the last admitted mutation; a timeout is retried only because the observation left the instance unchanged. The host evaluator, not the verifier, decides whether a run is verified.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-verifier.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`verifier/ref`](#field-verifier-ref) | `yes` | unspecified |  |
| [`checks`](#field-checks) | `yes` | array |  |
| [`timeout/ms`](#field-timeout-ms) | `yes` | integer |  |
| [`retry/max`](#field-retry-max) | `yes` | integer |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-verifier.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-verifier-ref"></a>
## `verifier/ref`

- Required: `yes`
- Shape: unspecified

<a id="field-checks"></a>
## `checks`

- Required: `yes`
- Shape: array

<a id="field-timeout-ms"></a>
## `timeout/ms`

- Required: `yes`
- Shape: integer

<a id="field-retry-max"></a>
## `retry/max`

- Required: `yes`
- Shape: integer
