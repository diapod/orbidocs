# Corpus Reasoning Experiment Proposal v1

Source schema: [`doc/schemas/corpus-reasoning-experiment-proposal.v1.schema.json`](../../schemas/corpus-reasoning-experiment-proposal.v1.schema.json)

## Governing Basis

- [`doc/project/60-solutions/038-corpus/038-corpus.md`](../../project/60-solutions/038-corpus/038-corpus.md)
- [`doc/project/60-solutions/047-agent/047-agent.md`](../../project/60-solutions/047-agent/047-agent.md)
- [`doc/project/40-proposals/064-inquirium-implementation-recommendations.md`](../../project/40-proposals/064-inquirium-implementation-recommendations.md)
- [`doc/project/60-solutions/046-sensorium-interfaces/046-sensorium-interfaces.md`](../../project/60-solutions/046-sensorium-interfaces/046-sensorium-interfaces.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)

### Stories

- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-009-bielik-blog-arca.md`](../../project/30-stories/story-009-bielik-blog-arca.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`proposal/ref`](#field-proposal-ref) | `yes` | string |  |
| [`query/id`](#field-query-id) | `yes` | string |  |
| [`room/id`](#field-room-id) | `yes` | string |  |
| [`turn/id`](#field-turn-id) | `yes` | string |  |
| [`author`](#field-author) | `yes` | ref: `corpus-reasoning-room-policy.v1.schema.json#/$defs/room-subject` |  |
| [`author/node-id`](#field-author-node-id) | `yes` | string |  |
| [`executor`](#field-executor) | `yes` | ref: `#/$defs/executor` |  |
| [`candidate-plan/ref`](#field-candidate-plan-ref) | `yes` | string |  |
| [`candidate-plan/artifact-ref`](#field-candidate-plan-artifact-ref) | `yes` | string |  |
| [`candidate-plan/digest`](#field-candidate-plan-digest) | `yes` | string |  |
| [`class/key`](#field-class-key) | `yes` | enum: `Public`, `Community`, `Personal` |  |
| [`human-in-loop/required`](#field-human-in-loop-required) | `yes` | const: `True` |  |
| [`proposed-at`](#field-proposed-at) | `yes` | string |  |
| [`expires-at`](#field-expires-at) | `yes` | string |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`executor`](#def-executor) | object |  |
| [`signature`](#def-signature) | object |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-proposal-ref"></a>
## `proposal/ref`

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

<a id="field-turn-id"></a>
## `turn/id`

- Required: `yes`
- Shape: string

<a id="field-author"></a>
## `author`

- Required: `yes`
- Shape: ref: `corpus-reasoning-room-policy.v1.schema.json#/$defs/room-subject`

<a id="field-author-node-id"></a>
## `author/node-id`

- Required: `yes`
- Shape: string

<a id="field-executor"></a>
## `executor`

- Required: `yes`
- Shape: ref: `#/$defs/executor`

<a id="field-candidate-plan-ref"></a>
## `candidate-plan/ref`

- Required: `yes`
- Shape: string

<a id="field-candidate-plan-artifact-ref"></a>
## `candidate-plan/artifact-ref`

- Required: `yes`
- Shape: string

<a id="field-candidate-plan-digest"></a>
## `candidate-plan/digest`

- Required: `yes`
- Shape: string

<a id="field-class-key"></a>
## `class/key`

- Required: `yes`
- Shape: enum: `Public`, `Community`, `Personal`

<a id="field-human-in-loop-required"></a>
## `human-in-loop/required`

- Required: `yes`
- Shape: const: `True`

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

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

## Definition Semantics

<a id="def-executor"></a>
## `$defs.executor`

- Shape: object

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
