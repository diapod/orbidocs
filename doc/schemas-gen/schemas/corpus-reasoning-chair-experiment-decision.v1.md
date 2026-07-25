# Corpus Reasoning Chair Experiment Decision v1

Source schema: [`doc/schemas/corpus-reasoning-chair-experiment-decision.v1.schema.json`](../../schemas/corpus-reasoning-chair-experiment-decision.v1.schema.json)

## Governing Basis

- [`doc/project/30-stories/story-012-agents-share-chair-terminal.md`](../../project/30-stories/story-012-agents-share-chair-terminal.md)
- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/60-solutions/038-corpus/038-corpus.md`](../../project/60-solutions/038-corpus/038-corpus.md)
- [`doc/project/60-solutions/047-agent/047-agent.md`](../../project/60-solutions/047-agent/047-agent.md)

## Project Lineage

### Stories

- [`doc/project/30-stories/story-012-agents-share-chair-terminal.md`](../../project/30-stories/story-012-agents-share-chair-terminal.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`decision/ref`](#field-decision-ref) | `yes` | string |  |
| [`query/id`](#field-query-id) | `yes` | string |  |
| [`room/id`](#field-room-id) | `yes` | string |  |
| [`proposal/ref`](#field-proposal-ref) | `yes` | string |  |
| [`review/ref`](#field-review-ref) | `yes` | string |  |
| [`review/digest`](#field-review-digest) | `yes` | string |  |
| [`reviewed-candidate-plan/ref`](#field-reviewed-candidate-plan-ref) | `yes` | string |  |
| [`reviewed-candidate-plan/artifact-ref`](#field-reviewed-candidate-plan-artifact-ref) | `yes` | string |  |
| [`reviewed-candidate-plan/digest`](#field-reviewed-candidate-plan-digest) | `yes` | string |  |
| [`chair`](#field-chair) | `yes` | ref: `corpus-reasoning-room-policy.v1.schema.json#/$defs/room-subject` |  |
| [`chair/node-id`](#field-chair-node-id) | `yes` | string |  |
| [`chair-agent/ref`](#field-chair-agent-ref) | `no` | string |  |
| [`decision`](#field-decision) | `yes` | enum: `block`, `request-revision`, `admit-reviewed-candidate` |  |
| [`reason/code`](#field-reason-code) | `yes` | string |  |
| [`class/key`](#field-class-key) | `yes` | enum: `Public`, `Community`, `Personal` |  |
| [`decided-at`](#field-decided-at) | `yes` | string |  |
| [`expires-at`](#field-expires-at) | `yes` | string |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`signature`](#def-signature) | object |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-decision-ref"></a>
## `decision/ref`

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

<a id="field-proposal-ref"></a>
## `proposal/ref`

- Required: `yes`
- Shape: string

<a id="field-review-ref"></a>
## `review/ref`

- Required: `yes`
- Shape: string

<a id="field-review-digest"></a>
## `review/digest`

- Required: `yes`
- Shape: string

<a id="field-reviewed-candidate-plan-ref"></a>
## `reviewed-candidate-plan/ref`

- Required: `yes`
- Shape: string

<a id="field-reviewed-candidate-plan-artifact-ref"></a>
## `reviewed-candidate-plan/artifact-ref`

- Required: `yes`
- Shape: string

<a id="field-reviewed-candidate-plan-digest"></a>
## `reviewed-candidate-plan/digest`

- Required: `yes`
- Shape: string

<a id="field-chair"></a>
## `chair`

- Required: `yes`
- Shape: ref: `corpus-reasoning-room-policy.v1.schema.json#/$defs/room-subject`

<a id="field-chair-node-id"></a>
## `chair/node-id`

- Required: `yes`
- Shape: string

<a id="field-chair-agent-ref"></a>
## `chair-agent/ref`

- Required: `no`
- Shape: string

<a id="field-decision"></a>
## `decision`

- Required: `yes`
- Shape: enum: `block`, `request-revision`, `admit-reviewed-candidate`

<a id="field-reason-code"></a>
## `reason/code`

- Required: `yes`
- Shape: string

<a id="field-class-key"></a>
## `class/key`

- Required: `yes`
- Shape: enum: `Public`, `Community`, `Personal`

<a id="field-decided-at"></a>
## `decided-at`

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

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
