# Corpus Task-pack Experiment Admission Request v1

Source schema: [`doc/schemas/corpus-task-pack-experiment.admit.request.v1.schema.json`](../../schemas/corpus-task-pack-experiment.admit.request.v1.schema.json)

Request to admit a typed task-pack experiment (P094-022b): the signed proposal, review and Chair decision with the peers they came from, and the Room publication of the candidate from the proposal's own turn. The same chain posted again finds its admission and resumes its handoff; a new execution step needs a current authorization of the chain.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-experiment.admit.request.v1` |  |
| [`candidate-publication/ref`](#field-candidate-publication-ref) | `yes` | string |  |
| [`proposal/source-peer`](#field-proposal-source-peer) | `yes` | string |  |
| [`proposal`](#field-proposal) | `yes` | ref: `corpus-reasoning-experiment-proposal.v2.schema.json` |  |
| [`review/source-peer`](#field-review-source-peer) | `yes` | string |  |
| [`review`](#field-review) | `yes` | ref: `corpus-reasoning-experiment-review.v4.schema.json` |  |
| [`chair-decision/source-peer`](#field-chair-decision-source-peer) | `yes` | string |  |
| [`chair-decision`](#field-chair-decision) | `yes` | ref: `corpus-reasoning-chair-experiment-decision.v2.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-experiment.admit.request.v1`

<a id="field-candidate-publication-ref"></a>
## `candidate-publication/ref`

- Required: `yes`
- Shape: string

<a id="field-proposal-source-peer"></a>
## `proposal/source-peer`

- Required: `yes`
- Shape: string

<a id="field-proposal"></a>
## `proposal`

- Required: `yes`
- Shape: ref: `corpus-reasoning-experiment-proposal.v2.schema.json`

<a id="field-review-source-peer"></a>
## `review/source-peer`

- Required: `yes`
- Shape: string

<a id="field-review"></a>
## `review`

- Required: `yes`
- Shape: ref: `corpus-reasoning-experiment-review.v4.schema.json`

<a id="field-chair-decision-source-peer"></a>
## `chair-decision/source-peer`

- Required: `yes`
- Shape: string

<a id="field-chair-decision"></a>
## `chair-decision`

- Required: `yes`
- Shape: ref: `corpus-reasoning-chair-experiment-decision.v2.schema.json`
