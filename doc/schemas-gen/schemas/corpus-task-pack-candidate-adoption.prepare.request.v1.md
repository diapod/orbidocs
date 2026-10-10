# Corpus-task-pack-candidate-adoption.prepare.request.v1

Source schema: [`doc/schemas/corpus-task-pack-candidate-adoption.prepare.request.v1.schema.json`](../../schemas/corpus-task-pack-candidate-adoption.prepare.request.v1.schema.json)

Owner-resolved choices and exact preview approval; not experiment permission.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-candidate-adoption.prepare.request.v1` |  |
| [`query/id`](#field-query-id) | `yes` | ref: `corpus-authority-epoch.v1.schema.json#/$defs/query` |  |
| [`proposal/ref`](#field-proposal-ref) | `yes` | string |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-candidate-adoption.prepare.request.v1`

<a id="field-query-id"></a>
## `query/id`

- Required: `yes`
- Shape: ref: `corpus-authority-epoch.v1.schema.json#/$defs/query`

<a id="field-proposal-ref"></a>
## `proposal/ref`

- Required: `yes`
- Shape: string

<a id="field-operator-binding-ref"></a>
## `operator/binding-ref`

- Required: `yes`
- Shape: string
