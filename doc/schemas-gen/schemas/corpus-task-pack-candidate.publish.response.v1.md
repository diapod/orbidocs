# Corpus Task-pack Candidate Publication Response v1

Source schema: [`doc/schemas/corpus-task-pack-candidate.publish.response.v1.schema.json`](../../schemas/corpus-task-pack-candidate.publish.response.v1.schema.json)

The host's answer to a task-pack candidate publication: the publication record, with the Agent product, passage and Corpus inference-Flow binding it was verified against, and whether the same publication was found again.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-candidate.publish.response.v1` |  |
| [`replayed`](#field-replayed) | `yes` | boolean |  |
| [`publication`](#field-publication) | `yes` | ref: `#/$defs/publication` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`publication`](#def-publication) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-candidate.publish.response.v1`

<a id="field-replayed"></a>
## `replayed`

- Required: `yes`
- Shape: boolean

<a id="field-publication"></a>
## `publication`

- Required: `yes`
- Shape: ref: `#/$defs/publication`

## Definition Semantics

<a id="def-publication"></a>
## `$defs.publication`

- Shape: object
