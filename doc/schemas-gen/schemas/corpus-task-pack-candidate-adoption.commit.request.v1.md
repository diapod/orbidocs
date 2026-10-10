# Corpus-task-pack-candidate-adoption.commit.request.v1

Source schema: [`doc/schemas/corpus-task-pack-candidate-adoption.commit.request.v1.schema.json`](../../schemas/corpus-task-pack-candidate-adoption.commit.request.v1.schema.json)

Owner-resolved choices and exact preview approval; not experiment permission.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-candidate-adoption.commit.request.v1` |  |
| [`preview`](#field-preview) | `yes` | ref: `corpus-task-pack-candidate-adoption.v1.schema.json#/$defs/preview` |  |
| [`approved/digest`](#field-approved-digest) | `yes` | ref: `corpus-authority-epoch.v1.schema.json#/$defs/digest` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-candidate-adoption.commit.request.v1`

<a id="field-preview"></a>
## `preview`

- Required: `yes`
- Shape: ref: `corpus-task-pack-candidate-adoption.v1.schema.json#/$defs/preview`

<a id="field-approved-digest"></a>
## `approved/digest`

- Required: `yes`
- Shape: ref: `corpus-authority-epoch.v1.schema.json#/$defs/digest`
