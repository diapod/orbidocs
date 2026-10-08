# Corpus-task-pack-turn.status.v1

Source schema: [`doc/schemas/corpus-task-pack-turn.status.v1.schema.json`](../../schemas/corpus-task-pack-turn.status.v1.schema.json)

Bounded owner-state projection of a retained turn operation. Stage is a recovery checkpoint, not permission to repeat inference or publish. The optional outcome is package-owned, separately validated data. Diagnostics contain no private provider error or prompt.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-turn.status.v1` |  |
| [`query/id`](#field-query-id) | `yes` | ref: `corpus-task-pack-turn.prepare.request.v1.schema.json#/$defs/ref` |  |
| [`task-binding/ref`](#field-task-binding-ref) | `yes` | ref: `corpus-task-pack-turn.prepare.request.v1.schema.json#/$defs/ref` |  |
| [`operation/ref`](#field-operation-ref) | `yes` | ref: `corpus-task-pack-turn.prepare.request.v1.schema.json#/$defs/ref` |  |
| [`preview/ref`](#field-preview-ref) | `yes` | ref: `corpus-task-pack-turn.preview.v1.schema.json#/properties/preview~1ref` |  |
| [`state`](#field-state) | `yes` | ref: `corpus-task-pack-turn.commit.response.v1.schema.json#/properties/state` |  |
| [`stage`](#field-stage) | `yes` | enum: `prepared`, `role-admitted`, `agent-spawned`, `agent-bound`, `turn-prepared`, `awaiting-human`, `turn-open`, `overlay-admitted`, `flow-bound`, `corpus-bound`, `inputs-prepared`, `published`, `completed`, `refused`, `unknown` |  |
| [`agent/id`](#field-agent-id) | `yes` | ref: `corpus-task-pack-turn.prepare.request.v1.schema.json#/$defs/ref` |  |
| [`operator-question/ref`](#field-operator-question-ref) | `no` | ref: `corpus-task-pack-turn.prepare.request.v1.schema.json#/$defs/ref` |  |
| [`cleanup/state`](#field-cleanup-state) | `no` | enum: `pending`, `completed` | Owner cleanup is separate from the turn disposition; a refused or unknown turn can still require bounded cleanup reconciliation. |
| [`outcome`](#field-outcome) | `no` | object |  |
| [`diagnostic`](#field-diagnostic) | `no` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-turn.status.v1`

<a id="field-query-id"></a>
## `query/id`

- Required: `yes`
- Shape: ref: `corpus-task-pack-turn.prepare.request.v1.schema.json#/$defs/ref`

<a id="field-task-binding-ref"></a>
## `task-binding/ref`

- Required: `yes`
- Shape: ref: `corpus-task-pack-turn.prepare.request.v1.schema.json#/$defs/ref`

<a id="field-operation-ref"></a>
## `operation/ref`

- Required: `yes`
- Shape: ref: `corpus-task-pack-turn.prepare.request.v1.schema.json#/$defs/ref`

<a id="field-preview-ref"></a>
## `preview/ref`

- Required: `yes`
- Shape: ref: `corpus-task-pack-turn.preview.v1.schema.json#/properties/preview~1ref`

<a id="field-state"></a>
## `state`

- Required: `yes`
- Shape: ref: `corpus-task-pack-turn.commit.response.v1.schema.json#/properties/state`

<a id="field-stage"></a>
## `stage`

- Required: `yes`
- Shape: enum: `prepared`, `role-admitted`, `agent-spawned`, `agent-bound`, `turn-prepared`, `awaiting-human`, `turn-open`, `overlay-admitted`, `flow-bound`, `corpus-bound`, `inputs-prepared`, `published`, `completed`, `refused`, `unknown`

<a id="field-agent-id"></a>
## `agent/id`

- Required: `yes`
- Shape: ref: `corpus-task-pack-turn.prepare.request.v1.schema.json#/$defs/ref`

<a id="field-operator-question-ref"></a>
## `operator-question/ref`

- Required: `no`
- Shape: ref: `corpus-task-pack-turn.prepare.request.v1.schema.json#/$defs/ref`

<a id="field-cleanup-state"></a>
## `cleanup/state`

- Required: `no`
- Shape: enum: `pending`, `completed`

Owner cleanup is separate from the turn disposition; a refused or unknown turn can still require bounded cleanup reconciliation.

<a id="field-outcome"></a>
## `outcome`

- Required: `no`
- Shape: object

<a id="field-diagnostic"></a>
## `diagnostic`

- Required: `no`
- Shape: object
