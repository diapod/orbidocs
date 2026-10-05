# Corpus Reasoning Experiment Review v4

Source schema: [`doc/schemas/corpus-reasoning-experiment-review.v4.schema.json`](../../schemas/corpus-reasoning-experiment-review.v4.schema.json)

A reviewer's signed verdict over exactly one typed experiment proposal: its ref and digest and the exact candidate artifact it carries. `evidence-state/digest` names the evidence the reviewer saw, the executed-run records published to the Room, in place of the Story 012 terminal snapshot. A reviewer never supplies a replacement candidate: `request-regeneration` asks the solver for a new candidate, which is a new proposal that needs its own review. Whether a review, a Chair decision and a proposal belong together is decided by the Corpus relation gate, not by this schema.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)
- [`doc/project/30-stories/story-013-qmail-task-pack.md`](../../project/30-stories/story-013-qmail-task-pack.md)

## Project Lineage

### Stories

- [`doc/project/30-stories/story-013-qmail-task-pack.md`](../../project/30-stories/story-013-qmail-task-pack.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `4` |  |
| [`review/ref`](#field-review-ref) | `yes` | string |  |
| [`query/id`](#field-query-id) | `yes` | string |  |
| [`room/id`](#field-room-id) | `yes` | string |  |
| [`proposal/ref`](#field-proposal-ref) | `yes` | string |  |
| [`proposal/digest`](#field-proposal-digest) | `yes` | string |  |
| [`candidate`](#field-candidate) | `yes` | ref: `corpus-reasoning-experiment-proposal.v2.schema.json#/$defs/candidate` |  |
| [`reviewer`](#field-reviewer) | `yes` | ref: `corpus-reasoning-room-policy.v1.schema.json#/$defs/room-subject` |  |
| [`reviewer/node-id`](#field-reviewer-node-id) | `yes` | string |  |
| [`reviewer-turn/id`](#field-reviewer-turn-id) | `yes` | string |  |
| [`evidence-state/digest`](#field-evidence-state-digest) | `yes` | string |  |
| [`verdict`](#field-verdict) | `yes` | enum: `accept`, `reject`, `request-regeneration` |  |
| [`findings`](#field-findings) | `yes` | array |  |
| [`reviewed/patches`](#field-reviewed-patches) | `no` | ref: `corpus-task-pack-review-verdict.v1.schema.json#/$defs/patches` | Exact review claims covered by this signature. Historical reviews may omit them; new task-pack repair admission and recipe publication require complete coverage at the owning relation gate. Absence is never enriched into historical coverage. |
| [`class/key`](#field-class-key) | `yes` | enum: `Public`, `Community`, `Personal` |  |
| [`reviewed-at`](#field-reviewed-at) | `yes` | string |  |
| [`expires-at`](#field-expires-at) | `yes` | string |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | ref: `corpus-reasoning-experiment-proposal.v1.schema.json#/$defs/signature` |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `4`

<a id="field-review-ref"></a>
## `review/ref`

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

<a id="field-proposal-digest"></a>
## `proposal/digest`

- Required: `yes`
- Shape: string

<a id="field-candidate"></a>
## `candidate`

- Required: `yes`
- Shape: ref: `corpus-reasoning-experiment-proposal.v2.schema.json#/$defs/candidate`

<a id="field-reviewer"></a>
## `reviewer`

- Required: `yes`
- Shape: ref: `corpus-reasoning-room-policy.v1.schema.json#/$defs/room-subject`

<a id="field-reviewer-node-id"></a>
## `reviewer/node-id`

- Required: `yes`
- Shape: string

<a id="field-reviewer-turn-id"></a>
## `reviewer-turn/id`

- Required: `yes`
- Shape: string

<a id="field-evidence-state-digest"></a>
## `evidence-state/digest`

- Required: `yes`
- Shape: string

<a id="field-verdict"></a>
## `verdict`

- Required: `yes`
- Shape: enum: `accept`, `reject`, `request-regeneration`

<a id="field-findings"></a>
## `findings`

- Required: `yes`
- Shape: array

<a id="field-reviewed-patches"></a>
## `reviewed/patches`

- Required: `no`
- Shape: ref: `corpus-task-pack-review-verdict.v1.schema.json#/$defs/patches`

Exact review claims covered by this signature. Historical reviews may omit them; new task-pack repair admission and recipe publication require complete coverage at the owning relation gate. Absence is never enriched into historical coverage.

<a id="field-class-key"></a>
## `class/key`

- Required: `yes`
- Shape: enum: `Public`, `Community`, `Personal`

<a id="field-reviewed-at"></a>
## `reviewed-at`

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
- Shape: ref: `corpus-reasoning-experiment-proposal.v1.schema.json#/$defs/signature`
