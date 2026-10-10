# Operator-task-delegation-status.v1

Source schema: [`doc/schemas/operator-task-delegation-status.v1.schema.json`](../../schemas/operator-task-delegation-status.v1.schema.json)

Current use eligibility of the immutable mandate; no cached authorization.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-delegation-status.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`loop/query-id`](#field-loop-query-id) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`mandate`](#field-mandate) | `yes` | unspecified |  |
| [`refusal`](#field-refusal) | `yes` | enum: `None`, `missing`, `revoked`, `expired`, `substituted`, `outside-scope`, `authority-lost` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-delegation-status.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-loop-query-id"></a>
## `loop/query-id`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-mandate"></a>
## `mandate`

- Required: `yes`
- Shape: unspecified

<a id="field-refusal"></a>
## `refusal`

- Required: `yes`
- Shape: enum: `None`, `missing`, `revoked`, `expired`, `substituted`, `outside-scope`, `authority-lost`
