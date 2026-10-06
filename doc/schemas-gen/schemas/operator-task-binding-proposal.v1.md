# Operator Task Binding Proposal v1

Source schema: [`doc/schemas/operator-task-binding-proposal.v1.schema.json`](../../schemas/operator-task-binding-proposal.v1.schema.json)

An exact, non-applied document for operator-owned read-only sources. It is not a commit receipt, activation or authorization. The source owner must explicitly edit the selected source; a consumer must not install a second hidden copy.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `operator-task-binding-proposal.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`disposition`](#field-disposition) | `yes` | const: `not-applied` |  |
| [`reason`](#field-reason) | `yes` | const: `operator-source-edit-required` |  |
| [`binding/ref`](#field-binding-ref) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/ref` |  |
| [`proposed/binding`](#field-proposed-binding) | `yes` | ref: `operator-task-local-binding.v1.schema.json` |  |
| [`proposed/digest`](#field-proposed-digest) | `yes` | ref: `operator-task-common.v1.schema.json#/$defs/digest` |  |
| [`expected/binding-digest`](#field-expected-binding-digest) | `yes` | unspecified |  |
| [`source/refs`](#field-source-refs) | `yes` | array |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `operator-task-binding-proposal.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-disposition"></a>
## `disposition`

- Required: `yes`
- Shape: const: `not-applied`

<a id="field-reason"></a>
## `reason`

- Required: `yes`
- Shape: const: `operator-source-edit-required`

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/ref`

<a id="field-proposed-binding"></a>
## `proposed/binding`

- Required: `yes`
- Shape: ref: `operator-task-local-binding.v1.schema.json`

<a id="field-proposed-digest"></a>
## `proposed/digest`

- Required: `yes`
- Shape: ref: `operator-task-common.v1.schema.json#/$defs/digest`

<a id="field-expected-binding-digest"></a>
## `expected/binding-digest`

- Required: `yes`
- Shape: unspecified

<a id="field-source-refs"></a>
## `source/refs`

- Required: `yes`
- Shape: array
