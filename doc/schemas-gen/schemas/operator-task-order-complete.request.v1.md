# Operator Task Order Complete Request v1

Source schema: [`doc/schemas/operator-task-order-complete.request.v1.schema.json`](../../schemas/operator-task-order-complete.request.v1.schema.json)

Explicit local operator approval of one exact verified recipe preview for an already linked order. All source, answer and provenance bytes are resolved by their owners, never supplied by this request.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-order-complete.request.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`order/ref`](#field-order-ref) | `yes` | ref: `operator-task-order-link.request.v1.schema.json#/properties/order~1ref` |  |
| [`execution/ref`](#field-execution-ref) | `yes` | ref: `corpus-experiment-task-pack-execution.v1.schema.json#/properties/execution~1ref` |  |
| [`recipe/digest`](#field-recipe-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`local-binding/expected-digest`](#field-local-binding-expected-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-order-complete.request.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-order-ref"></a>
## `order/ref`

- Required: `yes`
- Shape: ref: `operator-task-order-link.request.v1.schema.json#/properties/order~1ref`

<a id="field-execution-ref"></a>
## `execution/ref`

- Required: `yes`
- Shape: ref: `corpus-experiment-task-pack-execution.v1.schema.json#/properties/execution~1ref`

<a id="field-recipe-digest"></a>
## `recipe/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-operator-binding-ref"></a>
## `operator/binding-ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-local-binding-expected-digest"></a>
## `local-binding/expected-digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`
