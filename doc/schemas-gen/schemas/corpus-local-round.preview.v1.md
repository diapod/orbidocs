# Corpus-local-round.preview.v1

Source schema: [`doc/schemas/corpus-local-round.preview.v1.schema.json`](../../schemas/corpus-local-round.preview.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-local-round.preview.v1` |  |
| [`federation/id`](#field-federation-id) | `yes` | string | Actual selected Node federation, pinned by the owner in the approved preview. |
| [`choices`](#field-choices) | `yes` | ref: `corpus-local-round.prepare.request.v1.schema.json` |  |
| [`prepared/at`](#field-prepared-at) | `yes` | string |  |
| [`valid/until`](#field-valid-until) | `yes` | string |  |
| [`task-binding/digest`](#field-task-binding-digest) | `yes` | string |  |
| [`profile/digest`](#field-profile-digest) | `yes` | string |  |
| [`participant/ref`](#field-participant-ref) | `yes` | string |  |
| [`topic/term`](#field-topic-term) | `yes` | string |  |
| [`taxonomy/digest`](#field-taxonomy-digest) | `yes` | string |  |
| [`policy`](#field-policy) | `yes` | ref: `corpus-reasoning-room-policy.v4.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-local-round.preview.v1`

<a id="field-federation-id"></a>
## `federation/id`

- Required: `yes`
- Shape: string

Actual selected Node federation, pinned by the owner in the approved preview.

<a id="field-choices"></a>
## `choices`

- Required: `yes`
- Shape: ref: `corpus-local-round.prepare.request.v1.schema.json`

<a id="field-prepared-at"></a>
## `prepared/at`

- Required: `yes`
- Shape: string

<a id="field-valid-until"></a>
## `valid/until`

- Required: `yes`
- Shape: string

<a id="field-task-binding-digest"></a>
## `task-binding/digest`

- Required: `yes`
- Shape: string

<a id="field-profile-digest"></a>
## `profile/digest`

- Required: `yes`
- Shape: string

<a id="field-participant-ref"></a>
## `participant/ref`

- Required: `yes`
- Shape: string

<a id="field-topic-term"></a>
## `topic/term`

- Required: `yes`
- Shape: string

<a id="field-taxonomy-digest"></a>
## `taxonomy/digest`

- Required: `yes`
- Shape: string

<a id="field-policy"></a>
## `policy`

- Required: `yes`
- Shape: ref: `corpus-reasoning-room-policy.v4.schema.json`
