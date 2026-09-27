# Operator Task Profile Change Result v1

Source schema: [`doc/schemas/operator-task-profile-change-result.v1.schema.json`](../../schemas/operator-task-profile-change-result.v1.schema.json)

Per-axis diff between a binding's accepted task profile and the one its package now pins, each change classified as narrowing, widening or substitution, and whether the binding now follows the new profile. Values are enum names, numbers as text, or refs and digests; never local paths.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-profile-change-result.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`from/digest`](#field-from-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`to/digest`](#field-to-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`changes`](#field-changes) | `yes` | array |  |
| [`accepted`](#field-accepted) | `yes` | boolean |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-profile-change-result.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-from-digest"></a>
## `from/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-to-digest"></a>
## `to/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-changes"></a>
## `changes`

- Required: `yes`
- Shape: array

<a id="field-accepted"></a>
## `accepted`

- Required: `yes`
- Shape: boolean
