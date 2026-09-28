# Operator Task Verifier Result v1

Source schema: [`doc/schemas/operator-task-verifier-result.v1.schema.json`](../../schemas/operator-task-verifier-result.v1.schema.json)

What one verifier run observed: each named check with `pass` or `fail` and bounded observations. It is observation data, never a verdict: the host evaluator requires exactly the checks the verifier declares, and the task pack's own result schema may narrow this contract further.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-verifier-result.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`verifier/ref`](#field-verifier-ref) | `yes` | unspecified |  |
| [`checks`](#field-checks) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`check`](#def-check) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-verifier-result.v1`

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

## Definition Semantics

<a id="def-check"></a>
## `$defs.check`

- Shape: object
