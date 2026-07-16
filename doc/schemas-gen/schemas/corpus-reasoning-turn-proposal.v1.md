# Corpus Reasoning Turn Proposal v1

Source schema: [`doc/schemas/corpus-reasoning-turn-proposal.v1.schema.json`](../../schemas/corpus-reasoning-turn-proposal.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/073-agent-orchestration-organ.md`](../../project/40-proposals/073-agent-orchestration-organ.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`turn/id`](#field-turn-id) | `yes` | string |  |
| [`query/id`](#field-query-id) | `yes` | string |  |
| [`room/id`](#field-room-id) | `yes` | string |  |
| [`participant`](#field-participant) | `yes` | ref: `corpus-reasoning-room-policy.v1.schema.json#/$defs/room-subject` |  |
| [`assignment/id`](#field-assignment-id) | `yes` | string |  |
| [`turn/no`](#field-turn-no) | `yes` | integer |  |
| [`kind`](#field-kind) | `yes` | enum: `chair-prompt`, `expert-contribution`, `chair-synthesis` | Semantic role of the inert turn. The current Room-attested participant profile admits only expert-contribution; chair-prompt and chair-synthesis are reserved for a chair-specific dispatch path. |
| [`content/type`](#field-content-type) | `yes` | const: `text/plain` |  |
| [`content`](#field-content) | `yes` | string |  |
| [`content/digest`](#field-content-digest) | `yes` | string |  |
| [`class/key`](#field-class-key) | `yes` | enum: `Public`, `Community`, `Personal` |  |
| [`proposed-at`](#field-proposed-at) | `yes` | string |  |
| [`expires-at`](#field-expires-at) | `yes` | string |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | string |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-turn-id"></a>
## `turn/id`

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

<a id="field-participant"></a>
## `participant`

- Required: `yes`
- Shape: ref: `corpus-reasoning-room-policy.v1.schema.json#/$defs/room-subject`

<a id="field-assignment-id"></a>
## `assignment/id`

- Required: `yes`
- Shape: string

<a id="field-turn-no"></a>
## `turn/no`

- Required: `yes`
- Shape: integer

<a id="field-kind"></a>
## `kind`

- Required: `yes`
- Shape: enum: `chair-prompt`, `expert-contribution`, `chair-synthesis`

Semantic role of the inert turn. The current Room-attested participant profile admits only expert-contribution; chair-prompt and chair-synthesis are reserved for a chair-specific dispatch path.

<a id="field-content-type"></a>
## `content/type`

- Required: `yes`
- Shape: const: `text/plain`

<a id="field-content"></a>
## `content`

- Required: `yes`
- Shape: string

<a id="field-content-digest"></a>
## `content/digest`

- Required: `yes`
- Shape: string

<a id="field-class-key"></a>
## `class/key`

- Required: `yes`
- Shape: enum: `Public`, `Community`, `Personal`

<a id="field-proposed-at"></a>
## `proposed-at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires-at`

- Required: `yes`
- Shape: string

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `yes`
- Shape: string
