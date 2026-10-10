# Communication Authority Continuation Choices v1

Source schema: [`doc/schemas/corpus-authority-epoch.prepare.request.v1.schema.json`](../../schemas/corpus-authority-epoch.prepare.request.v1.schema.json)

Operator choices only. The owner resolves the admitted origin, current head, deadline, exact historical candidate material and producer evidence; no caller-authored digest establishes authority.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-authority-epoch.prepare.request.v1` |  |
| [`query/id`](#field-query-id) | `yes` | ref: `corpus-authority-epoch.v1.schema.json#/$defs/query` |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `yes` | string |  |
| [`retained/input-refs`](#field-retained-input-refs) | `yes` | array |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-authority-epoch.prepare.request.v1`

<a id="field-query-id"></a>
## `query/id`

- Required: `yes`
- Shape: ref: `corpus-authority-epoch.v1.schema.json#/$defs/query`

<a id="field-operator-binding-ref"></a>
## `operator/binding-ref`

- Required: `yes`
- Shape: string

<a id="field-retained-input-refs"></a>
## `retained/input-refs`

- Required: `yes`
- Shape: array
