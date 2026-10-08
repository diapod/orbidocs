# Corpus-task-pack-turn.commit.request.v1

Source schema: [`doc/schemas/corpus-task-pack-turn.commit.request.v1.schema.json`](../../schemas/corpus-task-pack-turn.commit.request.v1.schema.json)

Approval of one retained exact preview. The host checks the digest, original operator identity, bounded review window and current owner facts before any new mutation. Idempotent recovery does not regain revoked authority.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-turn.commit.request.v1` |  |
| [`preview/ref`](#field-preview-ref) | `yes` | string |  |
| [`approved/digest`](#field-approved-digest) | `yes` | ref: `corpus-task-pack-turn.prepare.request.v1.schema.json#/$defs/digest` |  |
| [`operator/binding-ref`](#field-operator-binding-ref) | `yes` | unspecified |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-turn.commit.request.v1`

<a id="field-preview-ref"></a>
## `preview/ref`

- Required: `yes`
- Shape: string

<a id="field-approved-digest"></a>
## `approved/digest`

- Required: `yes`
- Shape: ref: `corpus-task-pack-turn.prepare.request.v1.schema.json#/$defs/digest`

<a id="field-operator-binding-ref"></a>
## `operator/binding-ref`

- Required: `yes`
- Shape: unspecified
