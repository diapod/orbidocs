# Corpus-task-pack-candidate-adoption.commit.response.v1

Source schema: [`doc/schemas/corpus-task-pack-candidate-adoption.commit.response.v1.schema.json`](../../schemas/corpus-task-pack-candidate-adoption.commit.response.v1.schema.json)

Owner-resolved choices and exact preview approval; not experiment permission.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-candidate-adoption.commit.response.v1` |  |
| [`adoption`](#field-adoption) | `yes` | ref: `corpus-task-pack-candidate-adoption.v1.schema.json` |  |
| [`replayed`](#field-replayed) | `yes` | boolean |  |
| [`effects/authorized`](#field-effects-authorized) | `yes` | const: `False` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-candidate-adoption.commit.response.v1`

<a id="field-adoption"></a>
## `adoption`

- Required: `yes`
- Shape: ref: `corpus-task-pack-candidate-adoption.v1.schema.json`

<a id="field-replayed"></a>
## `replayed`

- Required: `yes`
- Shape: boolean

<a id="field-effects-authorized"></a>
## `effects/authorized`

- Required: `yes`
- Shape: const: `False`
