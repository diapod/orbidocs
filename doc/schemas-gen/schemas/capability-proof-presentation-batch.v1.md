# Capability Proof Presentation Batch v1

Source schema: [`doc/schemas/capability-proof-presentation-batch.v1.schema.json`](../../schemas/capability-proof-presentation-batch.v1.schema.json)

Mixed capability proof presentation envelope. It lets a peer or relay present several independently verifiable capability proof artifacts in one transfer while preserving partial-success semantics: each item is validated, admitted, refused, and audited independently.

## Governing Basis

- [`doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`](../../project/40-proposals/025-seed-directory-as-capability-catalog.md)
- [`doc/project/40-proposals/076-federation-identity-and-network-selector.md`](../../project/40-proposals/076-federation-identity-and-network-selector.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)
- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)
- [`doc/project/50-requirements/requirements-011-dator-arca-contracts.md`](../../project/50-requirements/requirements-011-dator-arca-contracts.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)
- [`doc/project/30-stories/story-004-pod-client-onboarding.md`](../../project/30-stories/story-004-pod-client-onboarding.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-007-settlement-capable-node.md`](../../project/30-stories/story-007-settlement-capable-node.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `capability-proof-presentation-batch.v1` | Schema discriminator. MUST be exactly `capability-proof-presentation-batch.v1`. |
| [`batch/id`](#field-batch-id) | `yes` | string | Stable idempotency/correlation handle for this presentation attempt. |
| [`presented/at`](#field-presented-at) | `yes` | string | RFC 3339 timestamp supplied by the presenter. Receivers use their own clock for validity decisions. |
| [`correlation/id`](#field-correlation-id) | `no` | string |  |
| [`source/node-id`](#field-source-node-id) | `no` | string | Optional self-declared presenter node id. Transport-observed source remains the stronger local signal when available. |
| [`items`](#field-items) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`Item`](#def-item) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `capability-proof-presentation-batch.v1`

Schema discriminator. MUST be exactly `capability-proof-presentation-batch.v1`.

<a id="field-batch-id"></a>
## `batch/id`

- Required: `yes`
- Shape: string

Stable idempotency/correlation handle for this presentation attempt.

<a id="field-presented-at"></a>
## `presented/at`

- Required: `yes`
- Shape: string

RFC 3339 timestamp supplied by the presenter. Receivers use their own clock for validity decisions.

<a id="field-correlation-id"></a>
## `correlation/id`

- Required: `no`
- Shape: string

<a id="field-source-node-id"></a>
## `source/node-id`

- Required: `no`
- Shape: string

Optional self-declared presenter node id. Transport-observed source remains the stronger local signal when available.

<a id="field-items"></a>
## `items`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-item"></a>
## `$defs.Item`

- Shape: object
