# Corpus-local-round.commit.response.v1

Source schema: [`doc/schemas/corpus-local-round.commit.response.v1.schema.json`](../../schemas/corpus-local-round.commit.response.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-local-round.commit.response.v1` |  |
| [`replayed`](#field-replayed) | `yes` | boolean |  |
| [`preview/digest`](#field-preview-digest) | `yes` | string |  |
| [`query/id`](#field-query-id) | `yes` | string |  |
| [`room/id`](#field-room-id) | `yes` | string |  |
| [`state`](#field-state) | `yes` | const: `prepared` |  |
| [`participants/ready`](#field-participants-ready) | `yes` | const: `False` |  |
| [`loop/opened`](#field-loop-opened) | `yes` | const: `False` |  |
| [`effects/authorized`](#field-effects-authorized) | `yes` | const: `False` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-local-round.commit.response.v1`

<a id="field-replayed"></a>
## `replayed`

- Required: `yes`
- Shape: boolean

<a id="field-preview-digest"></a>
## `preview/digest`

- Required: `yes`
- Shape: string

<a id="field-query-id"></a>
## `query/id`

- Required: `yes`
- Shape: string

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: string

<a id="field-state"></a>
## `state`

- Required: `yes`
- Shape: const: `prepared`

<a id="field-participants-ready"></a>
## `participants/ready`

- Required: `yes`
- Shape: const: `False`

<a id="field-loop-opened"></a>
## `loop/opened`

- Required: `yes`
- Shape: const: `False`

<a id="field-effects-authorized"></a>
## `effects/authorized`

- Required: `yes`
- Shape: const: `False`
