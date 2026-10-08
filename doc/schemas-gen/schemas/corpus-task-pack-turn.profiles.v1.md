# Corpus-task-pack-turn.profiles.v1

Source schema: [`doc/schemas/corpus-task-pack-turn.profiles.v1.schema.json`](../../schemas/corpus-task-pack-turn.profiles.v1.schema.json)

Read-only projection of admitted Agent profile choices. Presence is not current authorization or readiness. Budget/controller data is displayed, never submitted as an operator override. The owner validates controller semantics; this projection is limited to 128 rows and a 64 KiB carrier.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-turn.profiles.v1` |  |
| [`profiles`](#field-profiles) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`budget`](#def-budget) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-turn.profiles.v1`

<a id="field-profiles"></a>
## `profiles`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-budget"></a>
## `$defs.budget`

- Shape: object
