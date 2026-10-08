# Corpus Task-pack Chain Inspection v1

Source schema: [`doc/schemas/corpus-task-pack-chain-inspection.v1.schema.json`](../../schemas/corpus-task-pack-chain-inspection.v1.schema.json)

Read-only, owner-verified exact records for a human Chair. The host verifies query, proposal, review and candidate bindings and resolves retained patch bytes using the reviewer evidence resolver. This inspection grants no execution authority. The composed carrier is bounded to 4 MiB by the owner and client; it is never truncated.

## Governing Basis

- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-chain-inspection.v1` |  |
| [`query/id`](#field-query-id) | `yes` | ref: `corpus-task-pack-turn.prepare.request.v1.schema.json#/$defs/ref` |  |
| [`proposal`](#field-proposal) | `yes` | ref: `corpus-reasoning-experiment-proposal.v2.schema.json` |  |
| [`review`](#field-review) | `yes` | ref: `corpus-reasoning-experiment-review.v4.schema.json` |  |
| [`decision`](#field-decision) | `no` | ref: `corpus-reasoning-chair-experiment-decision.v2.schema.json` |  |
| [`decision/window`](#field-decision-window) | `yes` | object | Owner-observed lifetime of the exact signed chain. Current does not grant authority: Chair and experiment admission recheck it independently. Expired records remain inspectable, never renewed in place. |
| [`candidate/material`](#field-candidate-material) | `yes` | unspecified | Owner projection used for reviewer evidence. Current producers wrap every candidate with structural review/phase, verified patches (empty for observation) and exact source commitments; the raw candidate branch retains historical validation only. Phase is not safety or admission. A client may decode retained base64 bytes for UTF-8 display without changing their source commitment. Not an assertion supplied by a caller. |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-chain-inspection.v1`

<a id="field-query-id"></a>
## `query/id`

- Required: `yes`
- Shape: ref: `corpus-task-pack-turn.prepare.request.v1.schema.json#/$defs/ref`

<a id="field-proposal"></a>
## `proposal`

- Required: `yes`
- Shape: ref: `corpus-reasoning-experiment-proposal.v2.schema.json`

<a id="field-review"></a>
## `review`

- Required: `yes`
- Shape: ref: `corpus-reasoning-experiment-review.v4.schema.json`

<a id="field-decision"></a>
## `decision`

- Required: `no`
- Shape: ref: `corpus-reasoning-chair-experiment-decision.v2.schema.json`

<a id="field-decision-window"></a>
## `decision/window`

- Required: `yes`
- Shape: object

Owner-observed lifetime of the exact signed chain. Current does not grant authority: Chair and experiment admission recheck it independently. Expired records remain inspectable, never renewed in place.

<a id="field-candidate-material"></a>
## `candidate/material`

- Required: `yes`
- Shape: unspecified

Owner projection used for reviewer evidence. Current producers wrap every candidate with structural review/phase, verified patches (empty for observation) and exact source commitments; the raw candidate branch retains historical validation only. Phase is not safety or admission. A client may decode retained base64 bytes for UTF-8 display without changing their source commitment. Not an assertion supplied by a caller.
