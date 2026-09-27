# Operator Task Refusal v1

Source schema: [`doc/schemas/operator-task-refusal.v1.schema.json`](../../schemas/operator-task-refusal.v1.schema.json)

A tabled P094 refusal as returned by operator task-pack routes: the code with its retry class and next operator action from the refusal table, and optionally which binding choices are missing or which asset caused it. It carries no prose, secrets or local paths.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-refusal.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`refusal/code`](#field-refusal-code) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/refusalCode` |  |
| [`retry-class`](#field-retry-class) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/retryClass` |  |
| [`next-action`](#field-next-action) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/nextAction` |  |
| [`missing/fields`](#field-missing-fields) | `no` | array |  |
| [`subject/ref`](#field-subject-ref) | `no` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-refusal.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-refusal-code"></a>
## `refusal/code`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/refusalCode`

<a id="field-retry-class"></a>
## `retry-class`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/retryClass`

<a id="field-next-action"></a>
## `next-action`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/nextAction`

<a id="field-missing-fields"></a>
## `missing/fields`

- Required: `no`
- Shape: array

<a id="field-subject-ref"></a>
## `subject/ref`

- Required: `no`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`
