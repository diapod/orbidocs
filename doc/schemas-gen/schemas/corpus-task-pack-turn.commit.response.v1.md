# Corpus-task-pack-turn.commit.response.v1

Source schema: [`doc/schemas/corpus-task-pack-turn.commit.response.v1.schema.json`](../../schemas/corpus-task-pack-turn.commit.response.v1.schema.json)

A bounded operation handle and owner-state projection. accepted is admission, not completion; awaiting-human and unknown never authorize model execution, effects or redispatch by themselves.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-turn.commit.response.v1` |  |
| [`operation/ref`](#field-operation-ref) | `yes` | ref: `corpus-task-pack-turn.prepare.request.v1.schema.json#/$defs/ref` |  |
| [`preview/ref`](#field-preview-ref) | `yes` | string |  |
| [`state`](#field-state) | `yes` | enum: `accepted`, `awaiting-human`, `running`, `completed`, `refused`, `unknown` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-turn.commit.response.v1`

<a id="field-operation-ref"></a>
## `operation/ref`

- Required: `yes`
- Shape: ref: `corpus-task-pack-turn.prepare.request.v1.schema.json#/$defs/ref`

<a id="field-preview-ref"></a>
## `preview/ref`

- Required: `yes`
- Shape: string

<a id="field-state"></a>
## `state`

- Required: `yes`
- Shape: enum: `accepted`, `awaiting-human`, `running`, `completed`, `refused`, `unknown`
