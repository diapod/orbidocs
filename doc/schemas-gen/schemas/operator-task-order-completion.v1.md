# Operator Task Order Completion v1

Source schema: [`doc/schemas/operator-task-order-completion.v1.schema.json`](../../schemas/operator-task-order-completion.v1.schema.json)

Immutable host-retained result of an explicitly approved recipe publication. This is not a delivery receipt. The completion ref hashes the JCS document without completion/ref; replay delivers the retained dispatch result without a new executor or publication.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-order-completion.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`completion/ref`](#field-completion-ref) | `yes` | string |  |
| [`source`](#field-source) | `yes` | ref: `operator-task-verified-recipe.v1.schema.json#/$defs/source` |  |
| [`recipe/digest`](#field-recipe-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`dispatch/id`](#field-dispatch-id) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`answer`](#field-answer) | `yes` | ref: `corpus-reasoning-answer.v2.schema.json` |  |
| [`dispatch/result`](#field-dispatch-result) | `yes` | ref: `service-dispatch-result.v2.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-order-completion.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-completion-ref"></a>
## `completion/ref`

- Required: `yes`
- Shape: string

<a id="field-source"></a>
## `source`

- Required: `yes`
- Shape: ref: `operator-task-verified-recipe.v1.schema.json#/$defs/source`

<a id="field-recipe-digest"></a>
## `recipe/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-dispatch-id"></a>
## `dispatch/id`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-answer"></a>
## `answer`

- Required: `yes`
- Shape: ref: `corpus-reasoning-answer.v2.schema.json`

<a id="field-dispatch-result"></a>
## `dispatch/result`

- Required: `yes`
- Shape: ref: `service-dispatch-result.v2.schema.json`
