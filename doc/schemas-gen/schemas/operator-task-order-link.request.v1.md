# Operator Task Order Link Request v1

Source schema: [`doc/schemas/operator-task-order-link.request.v1.schema.json`](../../schemas/operator-task-order-link.request.v1.schema.json)

Current local operator's explicit selection of one provider-owned round for a retained remote order. The host checks the exact selected profile, question and current binding before recording a unique immutable link. Does not open a loop, appoint a Chair or grant HIL.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-order-link.request.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`order/ref`](#field-order-ref) | `yes` | string |  |
| [`query/id`](#field-query-id) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`local-binding/expected-digest`](#field-local-binding-expected-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-order-link.request.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-order-ref"></a>
## `order/ref`

- Required: `yes`
- Shape: string

<a id="field-query-id"></a>
## `query/id`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-operator-binding-ref"></a>
## `operator/binding-ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-local-binding-expected-digest"></a>
## `local-binding/expected-digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`
