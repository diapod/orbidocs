# Corpus-local-round.prepare.response.v1

Source schema: [`doc/schemas/corpus-local-round.prepare.response.v1.schema.json`](../../schemas/corpus-local-round.prepare.response.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-local-round.prepare.response.v1` |  |
| [`preview`](#field-preview) | `yes` | ref: `corpus-local-round.preview.v1.schema.json` |  |
| [`preview/digest`](#field-preview-digest) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-local-round.prepare.response.v1`

<a id="field-preview"></a>
## `preview`

- Required: `yes`
- Shape: ref: `corpus-local-round.preview.v1.schema.json`

<a id="field-preview-digest"></a>
## `preview/digest`

- Required: `yes`
- Shape: string
