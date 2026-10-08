# Corpus-local-round.prepare.request.v1

Source schema: [`doc/schemas/corpus-local-round.prepare.request.v1.schema.json`](../../schemas/corpus-local-round.prepare.request.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-local-round.prepare.request.v1` |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `yes` | string |  |
| [`task-binding/ref`](#field-task-binding-ref) | `yes` | string |  |
| [`problem/text`](#field-problem-text) | `yes` | string |  |
| [`participants`](#field-participants) | `yes` | array |  |
| [`topic/term`](#field-topic-term) | `no` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-local-round.prepare.request.v1`

<a id="field-operator-binding-ref"></a>
## `operator/binding-ref`

- Required: `yes`
- Shape: string

<a id="field-task-binding-ref"></a>
## `task-binding/ref`

- Required: `yes`
- Shape: string

<a id="field-problem-text"></a>
## `problem/text`

- Required: `yes`
- Shape: string

<a id="field-participants"></a>
## `participants`

- Required: `yes`
- Shape: array

<a id="field-topic-term"></a>
## `topic/term`

- Required: `no`
- Shape: string
