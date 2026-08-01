# Corpus Reasoning Experiment Regeneration v1

Source schema: [`doc/schemas/corpus-reasoning-experiment-regeneration.v1.schema.json`](../../schemas/corpus-reasoning-experiment-regeneration.v1.schema.json)

Host-signed durable join between one reviewer-requested correction and the exact solver-authored successor proposal.

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
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Contract version. |
| [`regeneration/ref`](#field-regeneration-ref) | `yes` | string | Content-addressed identity of this host-signed regeneration join. |
| [`query/id`](#field-query-id) | `yes` | string | Corpus query whose deliberation produced both proposals. |
| [`room/id`](#field-room-id) | `yes` | string | Room in which the source review and regenerated proposal were authored. |
| [`source-proposal/ref`](#field-source-proposal-ref) | `yes` | ref: `#/$defs/proposal-ref` | Content-addressed source proposal rejected for regeneration. |
| [`source-proposal/digest`](#field-source-proposal-digest) | `yes` | ref: `#/$defs/digest` | Digest bound by source-proposal/ref. |
| [`source-candidate-plan/ref`](#field-source-candidate-plan-ref) | `yes` | ref: `#/$defs/candidate-plan-ref` | Logical reference of the source CandidatePlan. |
| [`source-candidate-plan/artifact-ref`](#field-source-candidate-plan-artifact-ref) | `yes` | ref: `#/$defs/artifact-ref` | Content-addressed artifact containing the source CandidatePlan. |
| [`source-candidate-plan/digest`](#field-source-candidate-plan-digest) | `yes` | ref: `#/$defs/digest` | Digest of the source CandidatePlan bytes. |
| [`source-review/ref`](#field-source-review-ref) | `yes` | string | Content-addressed V2 review whose verdict is request-regeneration. |
| [`source-review/digest`](#field-source-review-digest) | `yes` | ref: `#/$defs/digest` | Digest bound by source-review/ref. |
| [`correction-state/digest`](#field-correction-state-digest) | `yes` | ref: `#/$defs/digest` | Digest of the bounded correction capsule shared by the source review, regenerated proposal review, and this join. |
| [`solver`](#field-solver) | `yes` | ref: `corpus-reasoning-room-policy.v1.schema.json#/$defs/room-subject` | Room subject that authored the regenerated proposal. |
| [`solver/node-id`](#field-solver-node-id) | `yes` | string | Node identity that signed the solver-authored proposal. |
| [`solver-turn/id`](#field-solver-turn-id) | `yes` | string | Exact solver turn from which the regenerated proposal originated. |
| [`regenerated-proposal/ref`](#field-regenerated-proposal-ref) | `yes` | ref: `#/$defs/proposal-ref` | Content-addressed successor proposal authored by the solver. |
| [`regenerated-proposal/digest`](#field-regenerated-proposal-digest) | `yes` | ref: `#/$defs/digest` | Digest bound by regenerated-proposal/ref. |
| [`regenerated-candidate-plan/ref`](#field-regenerated-candidate-plan-ref) | `yes` | ref: `#/$defs/candidate-plan-ref` | Logical reference of the regenerated CandidatePlan. |
| [`regenerated-candidate-plan/artifact-ref`](#field-regenerated-candidate-plan-artifact-ref) | `yes` | ref: `#/$defs/artifact-ref` | Content-addressed artifact containing the regenerated CandidatePlan. |
| [`regenerated-candidate-plan/digest`](#field-regenerated-candidate-plan-digest) | `yes` | ref: `#/$defs/digest` | Digest of the regenerated CandidatePlan bytes. |
| [`budget`](#field-budget) | `yes` | object | Host-admitted upper bounds for this regeneration attempt. |
| [`class/key`](#field-class-key) | `yes` | enum: `Public`, `Community`, `Personal` | Effective classification preserved across the regeneration chain. |
| [`host/node-id`](#field-host-node-id) | `yes` | string | Requester-host identity that admitted and signed this join. |
| [`created-at`](#field-created-at) | `yes` | string | Host timestamp at which the join was admitted. |
| [`expires-at`](#field-expires-at) | `yes` | string | Earliest expiry inherited from budget, source review, and regenerated proposal. |
| [`idempotency/key`](#field-idempotency-key) | `yes` | string | Requester-scoped command key used to replay the same registration safely. |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` | Domain-separated requester-host signature over this join. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`digest`](#def-digest) | string |  |
| [`proposal-ref`](#def-proposal-ref) | string |  |
| [`candidate-plan-ref`](#def-candidate-plan-ref) | string |  |
| [`artifact-ref`](#def-artifact-ref) | string |  |
| [`signature`](#def-signature) | object |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Contract version.

<a id="field-regeneration-ref"></a>
## `regeneration/ref`

- Required: `yes`
- Shape: string

Content-addressed identity of this host-signed regeneration join.

<a id="field-query-id"></a>
## `query/id`

- Required: `yes`
- Shape: string

Corpus query whose deliberation produced both proposals.

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: string

Room in which the source review and regenerated proposal were authored.

<a id="field-source-proposal-ref"></a>
## `source-proposal/ref`

- Required: `yes`
- Shape: ref: `#/$defs/proposal-ref`

Content-addressed source proposal rejected for regeneration.

<a id="field-source-proposal-digest"></a>
## `source-proposal/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

Digest bound by source-proposal/ref.

<a id="field-source-candidate-plan-ref"></a>
## `source-candidate-plan/ref`

- Required: `yes`
- Shape: ref: `#/$defs/candidate-plan-ref`

Logical reference of the source CandidatePlan.

<a id="field-source-candidate-plan-artifact-ref"></a>
## `source-candidate-plan/artifact-ref`

- Required: `yes`
- Shape: ref: `#/$defs/artifact-ref`

Content-addressed artifact containing the source CandidatePlan.

<a id="field-source-candidate-plan-digest"></a>
## `source-candidate-plan/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

Digest of the source CandidatePlan bytes.

<a id="field-source-review-ref"></a>
## `source-review/ref`

- Required: `yes`
- Shape: string

Content-addressed V2 review whose verdict is request-regeneration.

<a id="field-source-review-digest"></a>
## `source-review/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

Digest bound by source-review/ref.

<a id="field-correction-state-digest"></a>
## `correction-state/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

Digest of the bounded correction capsule shared by the source review, regenerated proposal review, and this join.

<a id="field-solver"></a>
## `solver`

- Required: `yes`
- Shape: ref: `corpus-reasoning-room-policy.v1.schema.json#/$defs/room-subject`

Room subject that authored the regenerated proposal.

<a id="field-solver-node-id"></a>
## `solver/node-id`

- Required: `yes`
- Shape: string

Node identity that signed the solver-authored proposal.

<a id="field-solver-turn-id"></a>
## `solver-turn/id`

- Required: `yes`
- Shape: string

Exact solver turn from which the regenerated proposal originated.

<a id="field-regenerated-proposal-ref"></a>
## `regenerated-proposal/ref`

- Required: `yes`
- Shape: ref: `#/$defs/proposal-ref`

Content-addressed successor proposal authored by the solver.

<a id="field-regenerated-proposal-digest"></a>
## `regenerated-proposal/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

Digest bound by regenerated-proposal/ref.

<a id="field-regenerated-candidate-plan-ref"></a>
## `regenerated-candidate-plan/ref`

- Required: `yes`
- Shape: ref: `#/$defs/candidate-plan-ref`

Logical reference of the regenerated CandidatePlan.

<a id="field-regenerated-candidate-plan-artifact-ref"></a>
## `regenerated-candidate-plan/artifact-ref`

- Required: `yes`
- Shape: ref: `#/$defs/artifact-ref`

Content-addressed artifact containing the regenerated CandidatePlan.

<a id="field-regenerated-candidate-plan-digest"></a>
## `regenerated-candidate-plan/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

Digest of the regenerated CandidatePlan bytes.

<a id="field-budget"></a>
## `budget`

- Required: `yes`
- Shape: object

Host-admitted upper bounds for this regeneration attempt.

<a id="field-class-key"></a>
## `class/key`

- Required: `yes`
- Shape: enum: `Public`, `Community`, `Personal`

Effective classification preserved across the regeneration chain.

<a id="field-host-node-id"></a>
## `host/node-id`

- Required: `yes`
- Shape: string

Requester-host identity that admitted and signed this join.

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

Host timestamp at which the join was admitted.

<a id="field-expires-at"></a>
## `expires-at`

- Required: `yes`
- Shape: string

Earliest expiry inherited from budget, source review, and regenerated proposal.

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `yes`
- Shape: string

Requester-scoped command key used to replay the same registration safely.

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

Domain-separated requester-host signature over this join.

## Definition Semantics

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-proposal-ref"></a>
## `$defs.proposal-ref`

- Shape: string

<a id="def-candidate-plan-ref"></a>
## `$defs.candidate-plan-ref`

- Shape: string

<a id="def-artifact-ref"></a>
## `$defs.artifact-ref`

- Shape: string

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
