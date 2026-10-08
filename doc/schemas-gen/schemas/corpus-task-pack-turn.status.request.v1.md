# Corpus-task-pack-turn.status.request.v1

Source schema: [`doc/schemas/corpus-task-pack-turn.status.request.v1.schema.json`](../../schemas/corpus-task-pack-turn.status.request.v1.schema.json)

Read-only inspection of one retained turn operation; no execution, authority renewal or retry is implied.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-turn.status.request.v1` |  |
| [`operation/ref`](#field-operation-ref) | `yes` | ref: `corpus-task-pack-turn.prepare.request.v1.schema.json#/$defs/ref` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-turn.status.request.v1`

<a id="field-operation-ref"></a>
## `operation/ref`

- Required: `yes`
- Shape: ref: `corpus-task-pack-turn.prepare.request.v1.schema.json#/$defs/ref`
